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

    sudo apt-get install -y --no-install-recommends \
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
    unixodbc

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

    with DAG(dag_id='simple_dag', start_date=days_ago(3),
            schedule_interval='@daily',
            catchup=True) as dag:
        task_1 = DummyOperator(task_id='task_1')

With this example DAG, one day after the start_date day will be the first runnig, by this, with catchup on True, **the DAG will got 3 runs.**
But if sou set catchup no **false**, **only the latest DAGruns will be automatically triggered by the scheduler**.
Using the same code block as example, with the start_date 3 days ago,but with catchup set up to false, you will got only **1 DAGrun**.

Also, you can limit the number of the past DAGruns active at the same time, using **max_active_runs**.

But with the CLI you cna also do the backfill by `airflows dags backfill`, even with catchup set to false. This is a good pratice

## 3.6 - Focus on Operators

A operator is a **task**, as soon you instantiate a operator in your DAG, will be a task.
If you have two tasks, like extracting data and cleaning data, **don't** put both on the same operator.
If cleaning data fails you will need to retry **both the tasks** as they are in the same operator. **one operator one task**.

To avoide reapeat your tasks you can set default arguments, applied to all of your operators. To do thhis you **create a dictionary outside the DAG** then into the dag parameters, set this dict to the `default_args=`
If you set a parameter in your task different that the default_args, the tassk parameter will have pioroity.

## 3.7 - Executing Python Functions

The most commom used operator in airflow!
`from airflow.operators.dummy import DummyOperator`
then you just create you task operator and use the `python_callable=` to start.
You can acess the context of your DAG using `**kwargs`on the python function. This return a dictionary with all your DAG info. But you can also pass directly args from the DAG dict, like "ds" from the start_date. To pass your own params, use the `op_kwargs=` as a dict of params.

## 3.8 - Puttin your DAG on hold

Sometimes you have to wait a specific file to land at a specific location before moving to the next task.
In airflow you can use the **File sensor**, a special kind of operator that wait something to happen before moving to the next task.
You import the sensor from `airflow.sensors.filesystem`then you set a specific parameter on you FileSensor task `fs_conn_id.
This fs_conn_id you create in the UI. Every time you handle with a outside system, you must create a connection there, that will be used in the operator.

**For example, if you want to interact with Presto** that doens't exist by default in Airflow, so you **must install the provider Presto** in order to get the connection type!
The **Extra** field is really important, like, if you want to connect into the AWS, is in the Extra field that you have to indicate an **acess key and sectret key!**, but also there is others ways to do that. **By default, what you put in Extra field is not hidden! Not secureted and you can see it in the UI**. The extra field expect a **JSON** value.
In the conn type file, the extra field expects the **folder where is the file exists**.
Even if the Extra field isn't secret, by default, both **Extra and password fields are encrypted** in the airflow db.

You can also changes the time that takes to check by changing the `poke_interval`, the default is 30 seconds.

## 3.9 - Executing Bash Commands

Bash operator is really simple, just need the **task_id** and the **bash_command** parameters.

## 3.10 - Define the path!

To define depedencies you can use two methods:
**- set_upstream** and;
**- set_downstream**.
I can just define **set_upstream** with a portuguese expression
Os últimos serao os primeiros!
Or the last ones will be the first ones...
So if we define `c.set_upstream(b)` and `b.set_upstream(a)` the path will be **a->b->c**.

For the set downstream is simple, as we set is the path to if `a.set_downstream(b)` and `b.set_dowstream(c)` the path will be **a->b->c**.

The way to read that is basicallly:
`execute_before.set_downstream(execute_after)`;
`execute_after.set_upstream(execute_before)`.

But, this ones is nome **commonly used in Airflow**
The better way to do that is by left and right bitshift operators, you can just do:
`a >> b >> c`
Much cleaner and clearer.
`>>` is for set_downstream , or `execute_before >> execute_after`;
and `<<` is for set_upstream, `execute_after << execute_before`.

**What if we have two tasks that we want to execute in the same time?**

Simple put the tasks into a list, if we want to execute B and C right after A:
`a >> [b, c]`

Also, you can use `from airflow.models.baseoperator import chain` to set a chain to the same as the previous example: `chain(a, [b, c])`

To create **cross dependencies** there is a special function call `cross_downdstream`:
If you try to create a cross dependecy with bitshift operator, you will got the error `unsupported operand types for list and list`. **You can't create a depedency between two list of tasks!**

## 3.11 - Exchanging Data

_xcom stands for cross communication_

**XComs** is the way to share data between your tasks. Allows you to share a small amount of data between then.
The simple way to do that is by simple returning a value from a python operator function.
To fetch this value you must acess the `ti` value in the other function, than call the method `ti.xcom_pull(key=, task_id=[''])`

We also can push xcom values by acessing the `ti` in the function we will share the data, and them use `ti.xcom_push(key='', value=)`

**Be aware**: the XCom is store into the database of Airflow, so they are limitied on sie, based on your used databse. **Don't process data (like terabytes of data) between your tasks using XComs**.
Airflow is not a processing framework!

## 3.12 - Ops... We got a failure

After a error, the tasks will wait the `retry_delay`, then retry the amount of times specified in the `retry`, in the default_args of the DAG or in the task specified ones.
If in the UI you click in **clear** after fix the error in the graph view the task will retry.

But if we got multiple DAGruns with multiple fields is better search specific for tasks marked to retry into list of task instance. You can also set a filter to dag_id to see specific dag marked to retry, after that, fix the issue, select the tasks, and clear, by this **you will retry all tasks at the same time**.
Always try to be specific whe na task have a failure, just retry the task, not all the DAGrun.

If you want to get alerted whe na task or a dag fails, you can use two paramters:
`email_on_failure` and `email_on_retry`. To do that you must specifcy a email with the param `email` and also configure the **SMTP** sever or you won't be able to send any email.

Let's say you want to execute something if a taks fails:
You can use the paramet `on_failure_callback` to execute something

# The Executor Kingdom

## 4.1 - The Default Executor

The **Sequential executor** is the default executor when you installed Airflow.
if we got like `t_1 >> [t_2, t_3] >> t_4`, with the sequential executor you can execute your tasks one after another, sequential, t*1 will run, then either t_2 or t_3 will get triggered, after both completed, finally t_4 is triggered. **You can't execut multiple tasks at the same time with the sequential executor**.
If you wan't to debug your tasks or do some experiments, the sequential executor \_might be pretty useful*.
Otherwise you basically never use it, because that executor it is quite **limited**.

## 4.2 - Concurrency, The parameters you must know!

There are a few aprameters you must know about that:

**Parallelism**: The maximum number of tasks you can execute at the same time in your _entire_ airflow instance, the dault value is **32**;

**DAG_concurrency** the number if taks of a given DAG that can be executed in parallel across all the DAGruns. The default is **16**;

**max_active_runs_per_dag** The number of DAGruns that can run at the same time for a given DAG. The default is also **16**.

## 4.3 - Start Scaling Apache Airflow

To run in production, you may want to execute more than on taks per time, which executor should you try first?

**The Local Executor**

Allow you to execute multiple tasks at the same time in your Airflow instance as long as you have **only yone machine**, just configure your db for postgres, as example, and change parameter executor to local executor and you are ready to start scaling in your own machine.
Yes, there are the limitation of the local executor in the Russel says you have on your single machine, unless you have a **quantic** machine you won't be able to run as many tasks as you want. At this point you will need another executor.

## 4.4 - Scaling to the Infinity!

**Celery executor** yo run task into a celery cluster (a distributed task queue to distribute your tasks into multiple machines).
You can have webserver and shcedule running in one node, postgress as DB running into another one, and in addition of the three core components, you also have the queue, with **celery workers** on separated machines, once you push a task, the task is pushed by the scheduler into the queue and then one of the workers will pusk the task inside the worker / machine. If you have more tasks to execute, you add another machine, that will be another worker, to execute more tasks in parallel.
