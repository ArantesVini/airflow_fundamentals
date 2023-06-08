NOTES:

# 0 - WELCOME

Airflow base components: - Web server; - Database; - Scheduler.

WHEN UPDATE AIRFLOW VERSION you must reastar airflow through astro dev stop && astro dev start;

# 1 - THE ESSENTIALS

## 1.1 - WHY AIRFLOW?

Extracting - > Transforming -> Loading
Extracting: Download from a API
Loading: In a DB
This is a data pipeline
CRON -> Isn't never the best choice to data pipelines, you cannot monitor it, cannot automatically run it, cannot retry, dont get warning. INSTEAD go with airflow to create, monitor a manager your data pipelines

## 1.2 - WHAT IS AIRFLOW?

is a open source plataforma to programmatically author, schedule, and monitor workflows!
Benefits: DYNAMIC, SCALABLE, HIGHLY INTEREACTIVE and EXTENSIBLE
but airflow IS NOT a streaming or data processing framework!
It's a orchestrator!

## 1.3 Core Components

### WEB SERVER : To acess the UI and monitor your pipelines in the best possible way;

### SCHEDULER : The heart of airflow, schedule and trigger any task, you can have mutiple scheduler running in multiple times;

### METADATA DATABASE: All metadata related to airflow is stored here, any database with SQLALchemy can used here.

#### !!!Non-core components!!!

#### EXECUTOR -> HOW your tasks is gone be executed, ex. CELERY for multiple machines, powerful machine for multiple tasks: LOCAL executor, default executor is SEQUENTIAL executor one task after another, and KUBERNETS for kubernets of course.

#### WORKER -> WHERE your task is executed, process and subprocess for local and kubernets executors.

## 1.4 - 2 Commom architectures

The two most commom with is:

### 1 - SINGLE NODE ARCHITETURE (One Node):

Web server, scheduler, metastore and executor run on the same machine!
Web server get all data that it needs from metastore, and if a task is ready to go scheduler check that in metastore and sent to executor (the queue of executor, to get fetch for the worker); As soon of the task id done, is stored in metastore! - The simplest architecture!

### 2 - MULTI NODES ARCHITECTURE (CELERY):

You can have different components in differente nodes! Like web server, scheduler and executor in one note and metastore and queue in another node. And you can also have a node just for workers

## 1.5 - CORE CONCEPTS

DAG's - Directed Acyclic Graph
The data pipeline, there is no loop between it, Tasks can deppend between that, but cannot depend with a task that depends on them.
OPERATOR s
The task in your DAG, is like a object arround the task you want to execute, there is three types: ACTIONS OPERATORES ( to execute something );
TRANSFER OPERATORS ( to transfer data from source to destination ); and
SENSOR OPERATOR ( when you want to wait something happen before run another task )
When a operator is associated in a DAG this operator become a TASK (a instance of an Operator);
When the task is ready to be scheduled, became a TASK INSTANCE OBJECT, that represent a specific run of a task: DAG + TASK + Point in time
DEPENDENCIES - The relation between your tasks and your operators
Functions are set_upstream OR set_dowstream, but the best iuse bid shift operator << OR >>, much cleaner!
WORKFLOW - Combination of all concepts
The DAG with the OPERATOR with the TASK!

## 1.6 - TASK LIFECYCLE

Web server -> Metastore -> Folder Dags -> Scheduler -> Executor

Create a new python file, like dag.py, into the folder Dags;
This file will be parsed both by web server and Scheduler ( Keep in min that web server parses DAGs everyu 30 seconds by default AND the Scheduler parses for new files (DAGS) every five minutes by default). If you don't see your DAG in the UI, you HAVE to wait 30 seconds to appear in the WS or then 5 minutes to run in the scheduler.
When the DAG is ready to be triggered the shceduelr createas a DAGRun object ( a instance of your DAG ), at the begginig a task in a DagRun object HAVE NO STATUS, then when a task is ready to be triggered, a TaskInstance object is created by scheduler, with the status SCHEDULED. Then the Scheduler sends the task into the executor, where the task has the status QUEUED, is when the executor is ready to take that task and execute it into a worker, and that is when the task is RUNNING, as soon as the task is done, the status of that task is SUCESS, resuming the task lifeclycle:

### No Staths -> Scheduled -> Queued -> Running -> Sucess

## 1.7 Installing Apache Airflow

Using Docker is undoubtedly the easiest way, but if you want to do that manually:

### 1 -> Python

    Must be 3.6+ at least

### 2 -> Pip

    You will use it to install Apache Airflow and all dependencies!

### 3 -> System dependecies (For linux users)

`sudo apt-get install -y --no-install-recommends \
 freetds-bin \
 krb5-user \
 ldap-utils \
 libffi6 \
 libsasl2-2 \
 libsasl2-modules \
 libssl1.1 \
 locales \
 lsb-release \
 sasl2-bin \
 sqlite3 \
 unixodbc`

### 4 -> Installing Apache Airflow

With pip install apache-airflow you will got a lot of a dependencies so is hard **recomended** to add a **constraint file**:
`export AIRFLOW_VERSION=2.5.1
export PYTHON_VERSION=3.8
pip install apache-airflow==${AIRFLOW_VERSION} --constraint https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt`
At this point, you already got Airflow installed, but to run it you must intialized first, there are two steps:

### 1: Generating the files and folders needed by Airflow (logs/, airflow.cfg, unitests.cfg etc.);

By default, the files and folders are generated in the folder ~/airflow

You can modify this behavior by setting the AIRFLOW_HOME environment variable.

For example, to initialize airflow in the folder /opt, export the following environment variable:
`AIRFLOW_HOME=/opt/airflow`

### 2: nitializing the metadata database (SQLite by default)

Once you're good with your Airflow home, initialize Airflow with:
`airflow db init`
Not you can run it!

## 1.8 - Extras and Providers

There are core dependencies, like email on failure or local executor to execute multiple tasks at the same time, but what if you want LDAP auth or execute task on Celery?
In that case you can extend the Core funcionalities of airflow, installing **extras**.
A extra is liek a provider with additional dependencies to extend the core funcionalities of airflow!
So what is a **provider** ?
A provider allow you to add funcionalities on Top of airflow, but a provider is **completely** separated of the Airflow Core, a provider **can** be updated without waiting for Airflow to be udpated.
For example if you want to connect with postgres, but you can't find it, cause isn't installed along with Airflow, you have to install the Postgress Provider.
So, what is the differences?
A extra is liek a package, all you need for run, in example, kubernets, but if you need just some operators or hooks, go for Providers

## 1.9 - Upgrading Apache Airflow

To don't get stuck in older versions, there is 5 steps:

### 1 - DB

Do a **backup** of Airflow metadata database, there are different ways, but taking a snapshot is the easiest one;

### 2 - DAGs

Check if there is no deprecated features in your DAGs, pause all of them and make sure no tasks are running. Because wou don't want to have anything being written into the DB while is upgraded.

### 3 - Upgradind Apache Airflow

`pip install "apache-airflow[any_extra]==2.0.1" --constraint constraint-file`

### 4 - Upgrade the DB

`airflow db upgrade`

### 5 - Restart

Restar the **web server, scheduler and worker(s)**

# 2 - INTERACTING WITH APACHE AIRFLOW

## 2.1 - THE 3 WAYS

There are three different ways to interact with Airflow:

### 1 - The User Interface (UI)

You will use this to manage and monitor your data pipelines, check the logs of the tasks, the history of your diagrams and etc...

### 2 - Command Line Interface (CLI)

This can be really useful in some special cases, for exempple, test your tasks, upgrade airflow, initialize airflow, and if you don't get acess to UI, you can use **CLI** to interact with airflow

### 3 - The REST API

Special usefull when you want to build something in top of Airflow, for example, when a Customer clicks a button, triggers a DAG.

There are lot of views, commands and endpoints on each of them!

## 2.2 - DAGs View

By default you use **admin** for both username and pswd, the first screen is the **DAGs View**.

With the **Toggle** you define when your DAG is ready to be scheduled or not. If the toggle is disabled, the scheduler isn't schedule your DAG!
Also in the UI, you can check the **Owner**, **Last Runs status**, **Schedule**, **Last Run info**, **Recent Tasks**, **Acions** where you can Trigger manually your dag ( The Toggle must be on ), refresh and **delete** your Dag ( this button don't remove the dag file, just all the metadata related to your Dag ), and the **Links** to acess other views, for example the **GRAPH VIEW** the **TREE VIEW**, **GANTT VIEW** and the **CODE VIEW**

## 2.3 - Tree View

**The history and current DAG view** along with the status of the task, you can quick spot a error in your tasks here, useful to spot a dag running late or error in your tasks

## 2.4 - Graph View

Perfect to check the dependencies of you data prepararing and the status of the tasks of the **late** DAG run, you also can see all tasks that will run and the order. The graph view is perfect to get a better view of your data plan and the relationships between all of the tasks. You **can** acess all the DAG run, selecting what DagRun your want
You also can see all the operators that are used. Also there is a auto-refresh button to see the last status of your tasks!

## 2.5 - Gantt View

The Gannt View **alows you to analyze taks duration**
as well all overlaps and bottlenecks on specific tasks. You can also use it to check if your tasks are **well running in parallel**. Larger the rectangle is the longer to complete the task! So, use the Gantt view to check **if your tasks are running in parallel** and if there is **any bottleneck in you diagrams**.

## 2.6 - Interacting with Tasks

By clicking in a task in nay of the views will appear the options to get **instance details, rendered button, logs and etc** and you can also run manually your tasks **if in the celery or kubernets executor**, **clear your task** after restart or retry a failured task.

## 2.7 - The Commands to Know

Another way to interact with airflow is by the **Command Line Interface, CLI** is extremly usefull to execute commands that are not avaliable in the UI or if you don't get acesss to the UI by some reason.
The main commands are:
By this you are inside the container of the component in the bash
`docker ps
docker exec -it {container id}/bin/bash`
To initialize the database of the airflow, you **must** enter this command first to also generate the files and folders needed by Airflow!`airflow db init`
If there is a new version of Airflow:
`airflow db upgrade`
Never use that in production, it removes **everything** in the database!:
`airflow db reset`
To start the webserver UI:
`airflow webserver`
To start the scheduler:
`airflow webserver`
To start a celery worker, in order to indicate that a machine can be used by airflow to execute tasks:
`airflow celery worker`
To pause/unpause dags, obviusly, if you to start or stop schedulling your dag:
`airflow dags pause / unpause`
To trigger a dag, if you don't have acess to the UI:
`airflow dags trigger`
you can also use **-e** to execute in a specific date

To see all your dags list
`airflow dags list`
To list the tasks of a specific DAG:
`airflow tasks list {dag_id}`
Use **every** time you add a new task into a DAG, to before push any DAGs in production you know if they really work`airflow tasks test {dag_id} {dag_id} {execution_date}`To rerun past DAGruns,`airflow dags backfill -s {start_date} -e {end_date} --reset_dagruns (dag_id)`

## 2.8 The REST API

**Stable** REST API, you can do all CRUD in this API to fully interact into DAG e DAGruns.
In the doc there is a full manual to check about the implementation of the API
_Actually you cannot do the D, delete the DAG from the API_
With this you can build new tools with Airflow!

# 3 - DAGs and Tasks

## 3.1 - DAG Skeleton

## 3.2 - Demystifing DAG Schedulling

Main parameters is
**start_date** define the date of your dag starts to be scheduled;
**schedule_interval** defines the frequency of the your dag will be triggered;
_Obs: your DAG is effectively triggered once the start_date **plus** the schedule interval is elapsed_

**Example**:
`In example if your start_date is like 01/01/2023 at 00:00 and your schedule_interval is 10 minutes, the first run will be 01/01/2023 at 00:10, but the **execution_date** is the first time, 00:00, after THIS 00:10 will be the **new start_date**, and after 10 minutes, at 00:20 the second DAGrun is created and runnign, and after it completes, the execution date of that DAGrun will be **00:10**`

**end_date** the date that wich your DAG won't be scheduled more.

## 3.3 - Playing with the start_date

By deffining the start_date dirrectly in your DAG object;
You can have different starts_date between your DAG and the tasks, but, actually, **there is no use case in that**, never do that.

** BY DEFAULT** all dates in Airlofw **Are stored in UTC**, and this is the best pratice, always store your dates in **UTC** to avoid problemns with timezone. If you want to do this in your current timezone you must put as UTC in DAG code.

You can also set a start*date in the future. But if this in the past, by default Airflow **will run all the non trigger DAGruns** between the current date and start date. *Be carefully with that!\*

_NEVER_ Define the start_date dinamically, like datetime.now(), cause every time the data pipeline is evalueted, the date will be modified!

## 3.4 - Playing with the schedule_interval

Your value of schedule interval can be a cron object **or** a timedelt object. By default this value is 24h. you can use _crontab.guru_ to check cron string expressions.
Time delts is best for days and weeks in general. You can also pass the value None to schedule_interval, doing this, you DAG will **never** be triggerd, this is really useful when you just want to manual / by API run you DAG!

## 3.5 - Backfilling and Catchup

**Backfilling** allows you to run a rerun past non triggered or arlready triggered DAGruns;
Ex: You made a mistkaed, you pause you DAG for five days, as soon as you fidex your issued, you want to resume you DAG, but in this period of your time you have non triggered DAG, so this DAGruns will be automatically triggered by AIrflow. You specify that with the parameter **catchup**, cathcup is _true by default_

```
with DAG(dag_id='simple_dag', start_date=days_ago(3),
         schedule_interval='@daily',
         catchup=True) as dag:
    task_1 = DummyOperator(task_id='task_1')
```

With this example DAG, one day after the start_date day will be the first runnig, by this, with catchup on True, **the DAG will got 3 runs.**
But if sou set catchup no **false**, **only the latest DAGruns will be automatically triggered by the scheduler**.
Using the same code block as example, with the start_date 3 days ago,but with catchup set up to false, you will got only **1 DAGrun**.

Also, you can limit the number of the past DAGruns active at the same time, using **max_active_runs**.

But with the CLI you cna also do the backfill by `airflows dags backfill`, even with catchup set to false. This is a good pratice

## 3.6 - Focus on Operators

## 3.7 - Executing Python Functions

## 3.8 - Puttin your DAG on hold

## 3.9 - Executing Bash Commands

## 3.10 - Define the path!

## 3.11 - Exchanging Data

## 3.12 - Ops... We got a failure
