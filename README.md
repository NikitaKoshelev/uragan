Django on OpenShift
===================

This git repository helps you get up and running quickly a Django
installation on OpenShift.

Running on OpenShift
--------------------

Create an account at https://www.openshift.com

Install the RHC client tools if you have not already done so:

    $ sudo gem install rhc
    $ rhc setup

Create a python application

    $ rhc app create <APP_NAME> python-3.3 postgresql-9.2 cron-1.4

Add this upstream repo

    $ cd <APP_NAME>
    $ git remote add upstream -m master git://github.com/NikitaKoshelev/uragan.git
    $ git pull -s recursive -X theirs upstream master

Then push the repo upstream

    $ git push

That's it. You can now checkout your application at:

    http://<APP_NAME>-<NAMESPACE>.rhcloud.com

Admin Interface
---------------

**login**: *demo*
**password**: *demo*
