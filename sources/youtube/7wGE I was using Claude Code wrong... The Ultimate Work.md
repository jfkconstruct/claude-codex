# 7wGE I was using Claude Code wrong... The Ultimate Work

Source: https://www.youtube.com/watch?v=UZb0if

For the past few weeks, I have
completely switched from cursor to cloud
code and learned a ton of things that
made my cloud code super effective. And
today, I will take you through how do I
use cloud code, how did I bring hero
type of specdriven demand process as
well as tips and practical examples of
how I use feature like hooks, custom
commands, and list of tips that made
myself much more effective. So, without
further ado, let's get started. But
before we dive into that, I know many of
you are just getting started learning
programming. And one question I got
asked a lot is what does road map look
like for learning code effectively.
That's why I want to introduce you to
this free ebook made by Google's
principal analytics lead and data
scientist where she wrote down all the
secret tips and methodologies that she
used to learn coding with claw and chatb
especially how she get output
personalized learning road map based on
her specific situation. It also cover
all the absolute fundamentals and basics
of coding like how do you choose the
right coding language to start with and
best practice prompt for different
coding scenario like debugging and
optimizing the code as well detailed
road map of how to master language like
Python in just four months. There's even
a custom GPT that has baking all the
core knowledge of latest package and
learning resource that you can talk to
alongside detailed video tutorial
showcasing her step-by-step work. So, I
definitely recommend you go take a look
if you're just getting started with your
coding journey. I put a link in the
description below for you to download
for free and thanks HubSpot for sharing
this awesome material with us. Now,
let's get back to how do I use cloud
code. So, first thing first, you want to
install this cloud code extension and
this will allow you to deeply integrate
into your current ID like cursor, VS
code or wingserf. So now I can click on
this run cloud code button and it will
automatically open cloud code in my
current ID and on the bottom right you
should see that it is detecting the
specific file I'm in and if I select
some lines it will also automatically
detect it. You can still use the
terminal here as well and you can just
do / IDE to choose the specific ID that
you wanted to connect to. Next the first
thing before you do anything is that you
should run this init command line. So
what this in command line do is that it
will get cloud start analyzing your
codebase to learn about what already set
up what are the kind of dependencies
components that you should be using. It
will also ask your permission to do
something for those type of commands
like cd I just don't care I will just
click on always auto approve and you
will see this thing is automatically
saved as permissions. I know some of you
actually want to get cloud code always
automatically run tools and there's a
way you can run that as well. You can do
this dangerously skip permissions and
this will show you that it is bypassing
all the permissions. So now tool it will
ask you for permission though I wouldn't
actually recommend this because from my
experience one of the key advantage of
the cloud codes UX is that allow you to
interact with cloud much better and I
will explain what I mean. All right so
after it scan finish it will try to
create this cloud MD file. If you're
using cursor, that's basically your
cursor rules. And if we click inside,
you can see that it automatically detect
what are the kind of tax stack, what are
the ROM build commands, the
architecture, the project structure, all
the useful stuff. So this give cloud a
very good base to continue developing
new things on top of this ripple. And
this cloud MD as I mentioned before is
pretty much the cursor rules. The only
difference is that in cursor the rules
are injected more programmatically. But
for cloud is much easier. Basically
every single run this text you define
here is appended on top of system
message and I know there are a lot of
people have different sorts of like a
cursor rules that to enhance the
workflow. For me it normally is pretty
simple. One prom I do add in is this
plan and review mode. This basically
tell cloud code that before we start
working on the project always in the
plan mode make a plan first. And for the
plan we want to save to this docloud
/task/taskname.md
so that we can keep track that later.
And inside this task, we should kind of
break down into different tasks. While
cloud code is doing its job, it should
also update the plan as we go and append
what it does into the doc. And this is
really useful because it is almost
always better to just align with cloud
code what exactly do you want. And this
kind of also similar to Amazon's new uh
kro workflow as well where they call it
like spec driven development. And what
it does is kind of similar. Uh it will
ask you to go through the requirements
and also kind of go through the
architecture design come up. It's
basically same thing and obviously you
can go as deep as like ko where you will
break down this three steps process but
I often found it's effective enough to
just do one kind of prd. So I will save
this and now we can get cloud code to
start implementing our feature. Normally
the first thing I would do is make a
plan. So our give prompt we are building
a beautiful online ID front end. help me
break down into key components and put
them together in the end. And here I'm
going to do shift tab. It will firstly
get into this auto accept edits mode,
but you want to shift tab again into
plan mode. So this plan mode is a really
really useful feature. When the agent is
in plan mode, it has this special system
prompt and limit access to tools. So it
will focus on doing things like web
search to understand the latest like tax
stack or documentations and also
planning the architecture and in the end
it will generate final reports and this
planning sometimes will take a while for
any feature that is semi complicated. I
would always do this plan mode first
back and forth a few times to align the
plan with cloud code and only after I
getting it start implementing the
feature. So here you will see that it is
showing task. When you see task it
basically means cloud code is calling a
sub aents that is specifically doing
this planning and research. So at
default cloud code has 17 different
tools that can do things like run
command line, read and find files, file
operations and web search. And this task
tool basically means it will launch a
new agent for keywords and file search.
When cloud code agent is calling this
task tool, it basically is creating
another agent that has almost all the
tool except those planning related tools
like task to-do and this agent will
receive a well-defined tasks from the
parent agent do a list of things and in
the end say here are the findings. Only
the last part which is summary of the
findings will be sent back to the parent
cloud code agent. And this is one
message they have to really save the
token consumption for the parent agent
because otherwise the main agent might
be flooded with all sorts of context.
And knowing this, you can actually
utilize this task to a lot better. For
example, you can actually prompt cloud
code to use task two to set up multiple
parallel agent to do different task at
the same time. But also if there's a
task that you know already, it's going
to read some very large files. Try to
prompt cloud code to just use task two
to do this because that will help you
save the token a lot on the main agent.
So now I finished the planning and come
back with a plan about what are the
layout system should look like file
explorer which makes sense the code
editor component it decide to use
existing library and then it will break
down into different phases. The phase
one is just install everything and the
phase two is implement file explorer
code editor terminal integration and
some advanced feature as well as the
project directory plan. So this is a
pretty good plan and obviously I can
keep planning but here I can also ask it
to start do this plan and next is that
it will create this detailed
implementation plan incloud/tasks
and I will click yes. So it will create
this task folder and create this online
ID front end with a detailed plan and
tasks. So now I can ask it to let's do
phase one. It will create a to-do based
on the phase one requirements. So while
it is running I'm just going to quickly
talk about this to-do. So I was quite
curious how did cloud code actually
handle this to-do. Do they handling to a
different like planner agent to just
specifically come up with plan and
programmatically get the agent to do one
task of another? So I did some
investigation. What I found is the
entropy team actually took the the
simplest setup possible. Uh but it's
really effective. It has this tool
called to-do right description is
basically use this tool to create and
manage and structure task list. They
have a very specific prompt talk about
like when to use this tool, when to not
use this tool, some example as well. So
every time when agent run this tool, it
will try to come up a list to-do and
each to-do will have the content ID,
priority and status. It is as simple as
this. So now if we come back here it
finish all the to-do it also going back
to our doc and adding details about what
it actually did. So it marked this as
completed and also document all the
things that it does. Cool. So it has
this component implemented that it has
this file explorer resizable. It has
terminal. I can add multiple different
terminal as well. Nice. Obviously you
can see I can continue going because it
already have trace of the overall plan.
So every time it just need to focus on
one specific piece of work and if there
any time when the plan change we can
just prompt it to update the stock. So
this is kind my like doc or spec focused
workflow with cloud code. But what's
really cool about cloud code is that you
can customize cloud code in very deep
manner. So one super interesting feature
is hooks. So hook is a feature that
allow you to define things to happen
programmatically when cloud code takes
certain actions. One of the most basic
and common hook that I use is this stop
hook. So I can define a rule here when
cloud code stop which means it finish
the task it try to run this command
which will basically play the system
sound to notify me that the task has
been completed. So with this one if I
just send a message to cloud it'll play
this notification sound after the task
is finished. So this is basically simple
concept of hook but interesting thing is
that the customization here can go
pretty deep. Cloud code allow you to
define things to do before or after
certain tool is wrong or when user try
to send a new message to cloud code so
that you can ingest some additional
context in as well as when cloud try to
compress the conversation history or
when a sub agent finishes task and
here's a more sophisticated example that
I found actually pretty useful. So I can
define this post to use hook that every
time after cloud code run a edit
multi-edit or write to which means it
modify or create some new files. It will
run this Python file I define here
called type check. So this is a feature
that I probably missed the most from
cursor is that in cursor it has this
automatic linked arrow detection and
this is really useful context so that
cursor can capture those errors even
before you run the code and proactively
fix issue. But for cloud it didn't have
this and this hook will basically
replicate that functionality directly.
So inside this Python file it might look
a bit complicated but I will quickly
explain to you what that means. So we
firstly try to get input data. Each hook
comes with a list of different inputs
that you can use. For example for the
post to use input it will automatically
give you a list data that you can use in
this like which tool it is what are the
input agent generate for this tool and
what's the output of tool. And in our
case, we want to get the file so we know
which file agent just created or
modified. Then we'll get a file pass.
And if this file extension is ts or tsx,
which means it's typescript, we will run
the type check. And if this type check
failed, this is a part where we can send
feedback back to cloud code. So you will
do the print and the file will be system
std error. Here I define code to be two.
So code two means that it is a blocking
arrow and std arrow will be fed back to
cloud code so that it can use that to
define the next actions. But you can
also define other asset code that will
still send message back to cloud code
but it won't blocking it from continue
the next action. So with this hook if
cloud code generates on files that has
type errors it will automatically call
the script and return back a error
message if it has any type. So cloud
code can try to proactively fix issue.
So this is how hook works and there are
a lot of potentials. For example, you
can even define some critic agent. After
cloud code write any code, it can write
a test and validate it or if it write
API doc, you can automatically update
documentations. I have included a few
common hooks that I use a lot in AI
builder club. So you can go and grab. If
you guys want a more deep dive or hook
feature, please comment below, let me
know. I'm happy to do another one. On
the outside, cloud code also have this
commands feature where they do come with
a list of predefined command like check
cost, set up MCP, memory, models and
review PR commands even, but they also
allow you to define custom slash
commands. For example, I can create a
commands folder under cloud and just
create something called joke MD and make
a joke in all caps. Once I did this, I
can do slash and search for joke. Then
this command I define here will be
showing up. If I click on that, whatever
you define here in this command will
basically be sent to cloud code almost
as a prompt. Network start behave based
on the rules you define there. I have
another video where I talk about
different commands that I predefined
that can help you extract specific
styling from a screenshots as well as
getting cloud code into design mode to
design multiple different UI iterations.
And you can even have a command to get a
cloud code to set up multiple different
git work tree to have sub agents working
in parallel. So you can go check out
this video if you want to learn more.
And there's a one package I thought is
pretty useful recently called
supercloud. It's a open source package
that comes with bunch of commands that
they predefine and build. For example, I
can do slash command SC analyze. This
will trigger that command that take
cloud into a much deeper code analyze
mode. It will create list of to-do to
look through the whole codebase and come
back with a kind of architecture review.
There are other useful things like you
can run workflow to look at a PRD doc to
get cloud into kind of step-by-step
implementation process as well as build
command that will help bundle and npm
build your projects as well as
troubleshoot if you have some weird bug
that you don't know how to fix. So this
is a really useful package even though
the installation is not that
straightforward. We need to open in a
folder do uv in it first to set up a
python project and then do uv as
supercloud. This will add this
supercloud package and in the end do UV
run Python supercloud install then it
will take you through the step-by-step
installation process but once you
install it will be installed at global
level so you don't need to keep doing
this and all the file will be basically
saved to your docloud settings at user
level if we open it it will basically
add stuff into the cloud MD which link
to all the different files that contain
more details inside this command folder
you can see all the commands that you
define here so this kind of quick
example of how far the customization you
can do with just command feature.
Meanwhile, the list of very useful
feature and shortcuts that cloud code
has that I didn't know initially.
Firstly, I can do slash resume to
jumping back to a past conversation
history and continue the conversation
there. This is kind of similar to cursor
where you can choose a past
conversation. But on the other hand,
they also introduces export command. So
this feature will allow you to copy the
whole conversation history with cloud
code. So you can jump between cloud
code, cursor, werf or any other coding
IDE because you just need to paste in
conversation history and no need to
worry that cursor don't have the context
about what has been done and quite often
I will also go to cloud where I have
unlimited amount token to do some early
exploration. Apart from that another
really useful feature is that you can
double tap exit and this will allow you
to revert back conversation history to a
past point. So you can just click that
and continue the conversation from that
point. This really good because
sometimes cloud code will make a
mistakes and this can avoid it. The only
downside is that if you're in cursor
when revert back to a past conversation
it will automatically revert back all
your files as well but cloud code didn't
keep a snapshot. So you actually need to
use some external package to do the
snapshot and versioning. One of them is
called CC undo. So this is a package
that will automatically detect all the
changes that cloud code has made to your
file and allow it to roll back. So I can
do CC undo and the list. This will list
out all the change that your cloud code
has been made and you can do CC undo
preview to see the specific change that
cloud code has been made and then once
you confirm you can do CC undo undo and
select a change you want to revert. So
this package can work with cloud code
handing pretty well. Though the command
line might not be the best and easiest
way for you to preview the work. There
are more userfriendly version like yo-yo
where it receive a snapshot and you can
add some additional instructions to
remember what the changes are. Another
quite useful shortcut is that you can
type in acceleration mark. And this will
get the cloud code into bash mode. So
bash mode allow you to run command
directly without going outside cloud
code. So I can do quickshot car like
pmppm install or pmppm add certain
package and it will just run the command
directly here. So it is really fast but
also the more important part is that
this context will be part of
conversation history so that cloud code
will know what are the actions that
you've been taken and similarly you can
also do hashtag which will activate the
memory mode. So here is where you can
type in things that you want cloud code
to memorize like I'm JSON we're building
online ID using chassis and component
and then it will ask you to choose where
do you want to save this memory it can
be per level or can be user level across
all the projects and once you confirm it
just save that information to the
cloudme and the last part I also want to
show you the easiest way for you to
connect cloud code to kim K2 model if
you don't know Kim K2 model is a new
open-source coding model that has
similar performance like cloud 3.5 to
cloud four but 80% cheaper. So it is
really good one to experiment if you run
out of credits. And the easiest way to
set up is that you can open terminal and
do code open this zshrc file. If you're
on Mac like me, you probably just do
this. But if you're on Windows, you
might need to change to bash. This will
open a file like this. So this will
basically control your terminal
behavior. So here I will define Kimi API
key. And don't worry, I already disabled
this key. So it's not going to work for
you guys anymore. And I can define kimi
where it will export entropic base URL
to moonshot using this API key and run
cloud. So with this one I can just go to
my any terminal and then do kimi. This
will open cloud code with the special
model that I defined there. So if I type
in hi here it is actually going to talk
to the kimi k2 model. And similarly you
can also define things here like claw
bash maintain per working directory to
be one. What this will do is that
basically every time when cloud is
running, it will always append the
current working directory into the
prompt. So it will always remember where
it is instead of running command in run
place. So here's a quick overview of how
I use cloud code. If you want to learn
more, you can join AI builder club where
we have weekly sessions to talk through
the latest workflow and tips for AI
coding and build large language models
as well as all detailed rules, hooks and
commands that I personally use. So you
can copy paste directly. In upcoming
weeks, we'll have more detailed
breakdown of how does a cloud code
actually work behind the scenes and try
to rebuild cloud code from scratch so
that we can learn the best practice of
building effective AI coding agents. I
put a link in the description below for
you to join. I hope you enjoy this
video. Thank you and I see you next
time.