#!/usr/bin/perl
#####################################################################################
# list dhcpd active leases 
#   - both "fixed" addresses which are normally not placed into leases database
#   - and dynamically given leases which are present in leases DB
# working for isc-dhcpd-server service but should also work for other compatible
# dhcpd servers. 
# produces HTML or CSV list of leases
#
# written by Marcin Gosiewski, BV Grupa s.c. Poland <marcin@gosiewski.pl>
# based on portions of code by Jason Antman <jason@jasonantman.com> 
#
# to make it work change the $logfilename and $leasedbname below and modify
# the regexp in second part of code (see below) to match your log lines format
# also you can optionally turn off reverse dns lookup (see below) which speeds up the process 
# of table creation and is useless unless you have reverse dns populated for 
# your fixed or dynamic leases
#
# CHANGELOG:
#     2017-03-13: initial version
use Socket;
use strict;
use warnings;
no warnings 'uninitialized';

# adjust this to match your files location: both log file and leases
# database. We use 2 last log files from logrotate, but you can add as many as you want
my @logfilenames = ( "/var/log/LOCALAPP.dhcpd.log.1", "/var/log/LOCALAPP.dhcpd.log" );
my $leasedbname = "/var/lib/dhcp/dhcpd.leases";
my %data = ();
# optional, can be modified to produce local time
use Time::Local;
use POSIX 'strftime';
my $now = time();
# local variables, lease information stored here
my $ip=""; 
my $status=""; 
my $interface=""; 
my $sdate="";         # beginning of lease
my $stime=""; 
my $edate="";         # end of lease
my $etime=""; 
my $adate="";         # last update (ACK) sent to requesting server
my $atime="";
my $mac=""; 
my $hostname="";
my $dnsname="";       # reverse dns lookup for host

#######################################################################
# first gather data from logfile for all ACK actions
#######################################################################

# collect all lines from log files into memory...
my @lines = (); my @loglines=(); 
foreach my $logfilename (@logfilenames)
{
  open LOGFILE, '<', $logfilename;
  chomp(@loglines = <LOGFILE>);
  #printf "LINES1: " . scalar @loglines . " in " .$logfilename . "\n";
  push(@lines, @loglines);
  close(LOGFILE);
}
@loglines=();
#printf "TOTAL LINES: " . scalar @lines . "\n";
foreach my $line (@lines)
{
  if ( $line !~ m/dhcpd: DHCPACK/) { next;}
  #printf "LINE: $line\n";

  ###############################
  # Modify the following line to make regexp capture 6 groups from log line:
  # 1 - date
  # 2 - time
  # 3 - ip 
  # 4 - mac
  # 5 - hostname if available
  # 6 - interface
  #$line =~ m/(^.{10})T(.{8}).+,\ dhcpd: DHCPACK on (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to ((?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}.*) via (.+)/;
  $line =~m/(^.{10})T(.{8}).+,\ dhcpd: DHCPACK on (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) to ((?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}) (.*)via (.+)/;
  # process the input
  $adate="$1";
  $atime="$2";
  $ip="$3";
  $mac="$4";
  $hostname="$5";
  $interface="$6";
  #add some 'known' facts:
  $status="ACK";
  $sdate="";    #"FOREVER";
  $stime="";
  $edate="";
  $etime="";

  #create/update record for this mac_addr
  #you can add extra check here if the IP address is not duplicated within
  #ack history and choose only the newer one. 

  $data{"$mac"}->{'ip'} = "$ip";
  $data{"$mac"}->{'status'} = "$status";
  $data{"$mac"}->{'interface'} = "$interface";
  $data{"$mac"}->{'adate'} = "$adate";
  $data{"$mac"}->{'atime'} = "$atime";
  $data{"$mac"}->{'sdate'} = "$sdate";
  $data{"$mac"}->{'stime'} = "$stime";
  $data{"$mac"}->{'edate'} = "$edate";
  $data{"$mac"}->{'etime'} = "$etime";
  $data{"$mac"}->{'mac'} = "$mac";
  $data{"$mac"}->{'hostname'} = "$hostname";
}
#close(LOGFILE);

#######################################################################
# gather data from lease database for dynamic addresses
# update the records (for existing) or add new records
#######################################################################

my $isdata = 0;
my $type = "";

#this information is not present in leases database so we just set
#it to default values
$interface="dhcpd";
$status="ACTIVE";
$adate="-";
$atime="";

open LEASEDB, $leasedbname or die $!;
foreach my $line (<LEASEDB>) 
{
  chomp($line);
  $isdata = 1 if $line =~ /^lease /;
  $isdata = 0 if $line =~ /^}/;

  if ($isdata) 
  {
    if ($line =~ /^lease/) 
    {
      $ip = (split(" ", $line))[1];
    } 
    elsif ($line =~ /^  starts/) 
    {
      ($sdate, $stime) = (split(" ", $line))[2,3];
      $sdate =~ s/\//-/g;
      $stime =~ s/;//;
    } 
    elsif ($line =~ /^  ends/) 
    {
      ($type, $edate, $etime) = (split(" ", $line))[1,2,3];
      if($type eq "never;")
      {
        $edate="forever";
        $etime=" ";
      }
      else
      {
        $edate =~ s/\//-/g;
        $etime =~ s/;//;
      }
    } 
    elsif ($line =~ /^  hardware ethernet/) 
    {
            $mac = (split(" ", $line))[2];
            $mac =~ s/;//;
    } 
    elsif ($line =~ /^  client-hostname/) 
    {
            $hostname = (split(/\"/, $line))[1];
    }
    elsif($mac ne "") 
    {
        #we have parsed the whole record, no more matching entries
        #data is collected to variables. now push the record.

        #now let's decide if we are updating the record or creating
        #new record

        # check against lease date, do not add expired leases
        # convert lease end time to local time/date and compare with $now
        my $y=0; my $m=0; my $d=0; my $H=0; my $M=0; my $S=0;
        my $edatetime = $now;
        ($y, $m, $d) = split("-", $edate);
        ($H, $M, $S) = split(":", $etime);
        $edatetime = timelocal($S,$M,$H,$d,$m-1,$y);
        if($edatetime >= $now)
        {
          # now check if record exists
          if(!defined($data{"$mac"}->{'mac'}))
          {
            #record does not exist, fill up default data
            $data{"$mac"}->{'mac'} = "$mac";
            $data{"$mac"}->{'interface'} = "$interface";
            $data{"$mac"}->{'ip'} = "$ip";
            $data{"$mac"}->{'hostname'} = "$hostname";
          }
          # record exists, let's check if we should update
          $data{"$mac"}->{'status'} = "$status";
          $data{"$mac"}->{'sdate'} = "$sdate";
          $data{"$mac"}->{'stime'} = "$stime";
          $data{"$mac"}->{'edate'} = "$edate";
          $data{"$mac"}->{'etime'} = "$etime";
          $data{"$mac"}->{'hostname'} = "$hostname";
          #we do NOT update ACK time because we do not have it
          #do NOT uncomment below
          #$data{"$mac"}->{'adate'} = "$adate";
          #$data{"$mac"}->{'atime'} = "$atime";

        }
    }
  }
}
close(LEASEDB);

#######################################################################
# sort data
#######################################################################

#we sort by IP but you can sort by anything.
my @sorted = sort { ($data{$a}{'ip'}) cmp ($data{$b}{'ip'}) } %data;

#######################################################################
# Print out everything to the HTML table
#######################################################################

my $hostnamelong="";

printf "Content-type: text/html\n\n";
printf "<html><head><title>Aktywne dzierzawy DHCP</title></head>\n";
printf "<style> table, th, td { border: 1px solid lightgray; border-collapse: collapse; padding: 3px; } ";
printf "tr:nth-child(even) { background-color: #dddddd; } ";
printf "</style>\n";
printf "<body>\n";
printf "<table border='1' cellpadding='6'>\n";
printf "<tr><th>IP</th><th>Status</th><th>Interface</th><th>Lease time</th><th>ACK time</th><th>Mac</th><th>Host</th></tr>\n";
foreach my $key (@sorted) {
    if($data{$key}{'mac'} eq "") { next ; }

    # BEGIN reverse dns lookup
    # can optionally turn off reverse dns lookup (comment out below lines) which speeds up the process 
    # of table creation and is useless unless you have reverse dns populated for 
    # your fixed or dynamic leases uncomment single line below instead:
    #
    # version without reverse dns lookup:
    # $hostnamelong = $data{$key}{'hostname'};
    #
    # version with reverse dns lookup: 
    # BEGIN
    $dnsname = gethostbyaddr(inet_aton($data{$key}{'ip'}), AF_INET);
    if($data{$key}{'hostname'} ne "")
    {
      $hostnamelong = $data{$key}{'hostname'} . " | " . $dnsname;
    }
    else
    {
      $hostnamelong = $dnsname;
    }
    $dnsname = "";
    # END

    printf "<tr>";
    printf "<td>" . $data{$key}{'ip'} ."</td>";
    printf "<td>" . $data{$key}{'status'} ."</td>";
    printf "<td>" . $data{$key}{'interface'} ."</td>";
    printf "<td>" . $data{$key}{'sdate'} . " " . $data{$key}{'stime'} ." - ";
    printf $data{$key}{'edate'} . " " . $data{$key}{'etime'} ."</td>";
    printf "<td>" . $data{$key}{'adate'} . " " . $data{$key}{'atime'} . "</td>";
    printf "<td>" . $data{$key}{'mac'} ."</td>";
    printf "<td>" . $hostnamelong ."</td>";
    printf "</tr>\n";
}

printf "</table>\n";
printf "</body></html>\n";

# END of program
