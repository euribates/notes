## Notes on uWSGI server

### Managing the uWSGI server

#### Starting the server

Starting an uWSGI server is the role of the system administrator, like starting the Web server. It
should not be the role of the Web server to start the uWSGI server – though you can also do that if
it fits your architecture.

How to best start uWSGI services at boot depends on the operating system you use.

On modern systems the following should hold true. On “classic” operating systems you can use
init.d/rc.d scripts, or tools such as Supervisor, Daemontools or inetd/xinetd.

You can instruct uWSGI to write the master process PID to a file with the safe-pidfile option.

#### Signals for controlling uWSGI

The uWSGI server responds to the following signals.

| Signal  | Description                     | Convenience command  |
|---------|---------------------------------|----------------------|
| SIGHUP  | gracefully reload all the workers and the master process | `--reload` |
| SIGTERM | brutally reload all the workers and the master process | (use --die-on-term to respect the convention of shutting down the instance) |
| SIGINT  | immediately kill the entire uWSGI stack | --stop |
| SIGQUIT | immediately kill the entire uWSGI stack ||
| SIGUSR1 | print statistics ||
| SIGUSR2 | print worker status or wakeup the spooler ||
| SIGURG  | restore a snapshot ||
| SIGTSTP | pause/suspend/resume an instance ||
| SIGWINCH| wakeup a worker blocked in a syscall (internal use) ||
| SIGFPE  | generate C traceback ||
| SIGSEGV | generate C traceback ||

Note: there are better ways to manage your instances than signals, as an example the master-fifo is
way more robust.

if you know the process is:

    kill -SIGHUP <proc_id>

#### Reloading the server

When running with the master process mode, the uWSGI server can be gracefully restarted without
closing the main sockets.

This functionality allows you patch/upgrade the uWSGI server without closing the connection with the
web server and losing a single request.

When you send the SIGHUP to the master process it will try to gracefully stop all the workers,
waiting for the completion of any currently running requests.

Then it closes all the eventually opened file descriptors not related to uWSGI.

Lastly, it binary patches (using execve()) the uWSGI process image with a new one, inheriting all of
the previous file descriptors.

The server will know that it is a reloaded instance and will skip all the sockets initialization,
reusing the previous ones.

There are several ways to make uWSGI gracefully restart.

    # using kill to send the signal
    kill -HUP `cat /tmp/project-master.pid`
    # or the convenience option --reload
    uwsgi --reload /tmp/project-master.pid
    # or if uwsgi was started with touch-reload=/tmp/somefile
    touch /tmp/somefile

Or from your application, in Python:

    uwsgi.reload()

Or in Ruby,

    UWSGI.reload

#### Stopping the server

If you have the uWSGI process running in the foreground for some reason, you can just hit CTRL+C to kill it off.

When dealing with background processes, you’ll need to use the master pidfile again. The SIGINT signal will kill uWSGI.

kill -INT `cat /tmp/project-master.pid`
# or for convenience...
uwsgi --stop /tmp/project-master.pid
The Master FIFO
Starting from uWSGI 1.9.17, a new management system has been added using unix named pipes (fifo): The Master FIFO
