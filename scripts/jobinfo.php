#!/usr/bin/env php
<?php
/* Helper script that retrieves information about jobs in the database
 *
 * Version 0.0.1
 */
require_once '/usr/share/xdmod/configuration/linker.php';

use CCR\DB;

function printarchiveinfo($dwDb, $job)
{
    $archivequery = "
SELECT
    h.hostname, a.filename 
FROM 
    modw_supremm.archive a, jobhosts jh, jobfact jf, hosts h 
WHERE 
    jf.job_id = ? AND 
    jh.job_id = jf.job_id AND
    jh.host_id = h.id AND
    a.hostid = h.id AND
    (
        (jf.start_time_ts BETWEEN a.start_time_ts AND a.end_time_ts)
        OR (jf.end_time_ts BETWEEN a.start_time_ts AND a.end_time_ts)
        OR (jf.start_time_ts < a.start_time_ts and jf.end_time_ts > a.end_time_ts)
        OR (CAST(jf.local_job_id_raw AS CHAR) = CAST(a.jobid AS CHAR))
    )
GROUP BY 1, 2 ORDER BY 1 ASC, a.start_time_ts ASC";

    $result = $dwDb->query($archivequery, array($job['job_id']));

    if (count($result) == 0) {
        print "There are no archives available for this job";
        return;
    }

    print "Archive list:\n";

    $lasthost = '';
    foreach ($result as $row) {
        if ($lasthost != $row['hostname']) {
            print "    Host \"${row['hostname']}\"\n";
            $lasthost = $row['hostname'];
        }
        print "      \"${row['filename']}\"\n";
    }
}

function printjobdata($resource, $localjobid)
{
    $dwDb = DB::factory('datawarehouse');

    $query = "
SELECT 
    job_id, FROM_UNIXTIME(start_time_ts) AS start, FROM_UNIXTIME(end_time_ts) AS end
FROM 
    jobfact jf, resourcefact r
WHERE
    r.code = ? AND jf.resource_id = r.id AND jf.local_jobid = ?";

    $result = $dwDb->query($query, array($resource, $localjobid));

    if (count($result) == 0) {
        print "Job $localjobid on $resource does not exist in the database.\n";
        return;
    }

    foreach ($result as $job) {

        $query = "
SELECT
    h.hostname
FROM
    jobhosts jh, hosts h
WHERE 
    jh.job_id = ? AND jh.host_id = h.id";

        $hosts = $dwDb->query($query, array($job['job_id']));

        if (count($hosts) == 0 ) {
            print "Job $localjobid (end time ${job['end']}) exists in the database, but has no host information.\n";
        } else {
            print "Job $localjobid (end time ${job['end']})\n";
            print 'Host list (' . count($hosts) . " hosts):\n";
            foreach ($hosts as $row) {
                print "    \"${row['hostname']}\"\n";
            }
            printarchiveinfo($dwDb, $job);
        }
        print "\n\n";
    }
}

function printhelp()
{
    print <<< EOF
Usage: php jobinfo.php [OPTION]...
Print information about a job or jobs in the database.

Mandatory arguments to long options are mandatory for short options too.
  -r, --resource=RESOURCE    select jobs for resource RESOURCE.
  -j, --jobid=JOBID          select jobs with job id JOBID.
  -h, --help                 print this help text.

EOF;
}

function printhint()
{
    $errmsg = <<< EOF
ERROR You must specify a resource and job id on the command line.  For example,
the following commandline will search for job 1234 on resource TEST:

    php jobinfo.php -r TEST -j 1234

You can also use the -h or --help options to display help text.

EOF;
    fwrite(STDERR, $errmsg);
}

function main()
{
    global $argv, $logger;

    $opts = array(
        array('h', 'help'),
        array('j:', 'jobid:'),
        array('r:', 'resource:'),
    );

    $shortOptions = implode('', array_map(function ($opt) { return $opt[0]; }, $opts));
    $longOptions = array_map(function ($opt) { return $opt[1]; }, $opts);

    $args = getopt($shortOptions, $longOptions);

    if ($args === false) {
        fwrite(STDERR, "ERROR Failed to parse arguments\n");
        exit(1);
    }

    $resource = null;
    $jobid = null;

    foreach ($args as $key => $value) {
        if (is_array($value)) {
            fwrite(STDERR, "ERROR Multiple values not allowed for '$key'\n");
            exit(1);
        }

        switch ($key) {
            case 'h':
            case 'help':
                printHelp();
                exit(0);
                break;
            case 'r':
            case 'resource':
                $resource = $value;
                break;
            case 'j':
            case 'jobid':
                $jobid = $value;
                break;
            default:
                fwrite(STDERR, "ERROR Unexpected option '$key'\n");
                exit(1);
                break;
        }
    }

    if ($resource === null && $jobid === null) {
        printhint();    
    } else {
        printjobdata($resource, $jobid);
    }
}


try {
    main();
} catch (Exception $e) {
    do {
        fwrite(STDERR, 'message: ' . $e->getMessage() . ' stack: ' . $e->getTraceAsString());
    } while ($e = $e->getPrevious());
    exit(1);
}
