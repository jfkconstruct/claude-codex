# I was wrong about Claude Code UPDATED AI workflow

Source: https://www.youtube.com/watch?v=gNR3XI5Eb0k

So, I wasn't sure if I should make this
video because I recently did a video two
months ago about my AI coding workflow,
but so much has changed in that time
that I felt like I had to do it. If
you're new here, welcome to the video.
My name is Chris and I build
productivity apps. And today, I'm going
to share my updated AI coding workflow.
So, if you saw my workflow video, you
know that I use Cursor and Cursor agents
to do the AI coding, which most
developers are currently using right
now. But I've recently switched to
Claude Code, and I basically haven't
used Cursor's AI features like agents in
over a week. In this video, we're going
to cover why I switched to Cloud Code.
my workflow and practical tips to get
the most out of cloud code and then some
general thoughts on where I think AI
coding is heading in general. Okay, so
what happened? Why did I change to cloud
code? So, I've been using cursor just
like everyone else for over a year now.
There's absolutely nothing wrong with
cursor, but about a week ago, Enthropic
introduced some new pricing to Claude
code. If you're not familiar, it is
basically a coding agent. So, it
actually lives in the terminal. So, it's
not a code editor like cursor. It just
lives in the terminal and you can put it
into any codebase and just ask it to do
anything. You can ask it questions. You
can ask it to add features. And I have
been genuinely surprised by the results
that I've been getting. A lot of these
things were things that cursor even with
Claude Opus for Max, which is again one
of the best models for coding, was
really struggling to help me with.
Claude Code was able to come up with
solutions to these issues really
quickly. It seemed to think about
complex problems way better than
cursor's agent. And the solutions it
came up with were genuinely better every
time I compared the two. So how does
this stuff actually work? Way it works
is you go to any project in your
terminal and then you just run the
claude command. And when you run this
command, you can start chatting with it.
You can ask it questions. You can tell
it to work on features. Exactly like
cursor agent. And my workflow barely
deviates from how I use cursor agent.
I'm just constantly asking the agent to
do things. I'm checking the code.
Technically, I am still using cursor,
but I'm not really using any of the AI
stuff. I just use cursor or Xcode as my
editor. And then I have Claude Code in a
terminal window. Usually on the right
side.
First thing is Claude Code does have
something called plan mode. So, if you
hit shift tab on your computer, you'll
see that it'll change to plan mode. And
what this is going to do is it's only
going to think through the problem, and
it's not going to actually generate or
modify any code. So, the way that I use
cloud code is I always first use plan
mode. I ask it to make a change. So, if
I ask it something like, can you go
modify this? I make sure I'm in plan
mode, I hit enter, and then it's going
to think through for a pretty long time
usually, and then it's going to spit out
its game plan. I review this game plan
very thoroughly and then if I'm happy
with it, I tell it, okay, go ahead, go
try to execute the plan. If not, I hit
no and then I revise the plan. And so
that's tip number one in step one in my
workflow is I always use plan mode
first. So number two is I always
generate a Claude MD file. So this is a
file that's basically the brain and the
memory of Claude when it's working on
your project. You can kind of think of
it like cursor rules. You're basically
giving Claude rules, but it is very
important and Claude really follows this
thoroughly. If you hit /init in any
codebase, it's actually going to
automatically generate this file for
you. And then you can go ahead and make
modifications or you can even tell cloud
code itself like, hey, can you remember
to do this next time? And it'll go ahead
and add to the claude MD file. So step
number two is generating this and making
sure that it's accurate and up to date
and exactly how I want it to be. So step
number three when I'm about to start
actually using it and modifying code is
I always make sure to commit frequently
and use Git as almost a checkpoint
system. So, if you're familiar with
cursor, they have this really nice
restore feature in the chat. You can go
anywhere back in your chat, hit the
restore button, and it'll basically go
back to that point in time of the chat.
It's really great when cursor agent is
going down the wrong path or you made a
mistake. And I was constantly using that
feature. Cloud code has nothing like
this. So, the way I'm getting around
this is by using git almost as my
checkpoint system. When I'm happy with
the changes, I make a commit and if I
don't like the changes, I just discard
or revert the commit. It's kind of a
hacky system and I haven't found a
better way to do this, but it gets the
job done. It gives me the ability to
undo changes if Claude does something
that I'm not happy with. Number four is
using screenshots. So, you can actually
drag screenshots into Claude code so
that way it has context. Very similar to
cursor agent. You can drag images into
the chat. I do this with errors. I do
this with design screenshots, but I'm
constantly dragging in images. Number
five is similar to images. I usually
also drag in entire folders. And I'm not
talking about folders in your codebase.
I'm talking about other folders in other
code bases. So something I'm frequently
doing for Ellie, for example, is I'm
working on the Ellie front end. I like
to drag in the folder for the back end
and tell it, hey, by the way, this is
what the back end looks like. I found it
is very helpful to give it additional
context on something like how does the
back end work? Can't actually make
changes to the folders if you give it
permission. So sometimes if I'm asking
it to build something on the front end,
it can go ahead and make changes for the
back end for me. I heard that working
with multiple codebases not officially
supported, but this is a way to get
around that. Number six is giving it
URLs. So something a lot of people don't
know is that claude code actually has
access to a web browser. So you can just
paste in the link to documentation kind
of similar to what you can do with
cursor. But when you give it the link to
documentation, it will go to the
website, read the documentation and get
whatever context that it needs. I can
also run Google searches and go find
documentation. So sometimes I just tell
it things like make sure to use the
latest Google calendar API and it'll
actually go do a web search and go find
the documentation. So I don't even have
to paste the link in. I'm constantly
doing that, especially when I'm working
with newer APIs. Number seven is
sometimes I use sub aents. Cloud code
has the ability to spin up sub aents. So
these are instances of cloud code with
their own context that will go off in
parallel. So if I'm doing a task that's
pretty massive, like trying to port an
entire LE iOS app to Android. I told it
for the sake of time, can you actually
break this problem down and run sub
agents where necessary? Actually spun up
like 10 agents that all ran in parallel
at the same time. If I ran this without
sub agents, this probably would have
taken over an hour to run. But since I
ran it with sub agents in parallel, they
all ran at the same time and it was able
to finish much faster. Number eight is
that I actually asked it to doublech
checkck its work. So when it's done, I
often ask it, hey, can you make sure
that it didn't break anything else or
can you try to find some edge cases and
just confirm that everything is working.
I've been surprised that sometimes it
actually does find things that I've
originally missed and it gives me a
little bit more peace of mind about the
code that it generated. Number nine,
which really isn't a tip, this is what I
do, is I always review the code that it
generates. This thing is so good that I
can easily see people just blindly
accepting whatever it's producing. But
my advice and for my workflow, I always
review the code that it produces almost
as if it was another developer and I'm
basically just kind of reviewing a pull
request and reviewing their changes. If
you're using any of these AI tools, you
should be doing that anyway. But I think
it's worth saying because especially
with Claude Code, this can get really
tempting to just blindly accept things
because it is really good at generating
some of this stuff.
I wanted to share some real examples of
things that I was able to build with
Claude code that I wasn't able to do
with cursor. Specifically, I've been
using cursor with claude sonnet 4 as the
model and sometimes I even use claude
opus for max, which is one of the most
expensive and powerful models on cursor
and it still wasn't able to get some of
these things. So, one example was very
custom drag and drop animations in the
LE iOS app. So, this is where you can
hold down and reorder list items. This
isn't using the default Swift UI drag
and drop. It's a completely custom drag
and drop experience which cursor did
seem to be struggling with after a
couple hours, but the minute I switched
to cloud code, it was able to get it in
like 30 minutes. Second example is a
feature in Ellie where you can take an
external calendar event like a Google
calendar event and convert it into a
task. I have been struggling with this
feature for over a year now because it
is extremely complex. It touches three
different calendar integrations. It
touches recurring tasks. It's just an
overall very complicated feature the way
that it's built into Ellie. Because of
the complexity, cursor had a really hard
time helping me with this. Every time it
changed something and something was
fixed, another thing ended up breaking.
But Cloud Code was able to deal with all
of that complexity and I was able to
successfully ship this in less than 1
hour. So the last example is a very
extreme one. I actually started the
process of porting over the Ellie iOS
app to Android. And I had attempted to
do this with Cursor in the past, but it
kind of struggled to do this because
this is a pretty big migration. Cloud
Code actually made substantial progress
and I was thoroughly surprised by the
results I got with this. If you don't
believe me on the timeline, I was live
tweeting the entire thing. So, you can
go check that out if you want some
proof. But these were three concrete
examples, but I had five or six other
features that I used as benchmarks to
test cursor versus cla code. And every
single time, Claude Code gave me better
results and much much faster than cursor
could. Cloud code has been around for a
few months now and I've heard really
good things. But the reason I was
hesitant to try it is it was only
available through API based pricing
which means I had to provide my own API
key and I had to pay based on the amount
of tokens that I was using with claude
code. And as someone who does a ton of
AI coding that scared me because I'd
rack up a huge bill if I use this the
same way I was using cursor. So I've
always stayed away from it until they
introduced their new $200 Claude Max
plan which allows you to have borderline
unlimited usage and not have to worry
about the tokenbased pricing. Obviously,
the big caveat is to use it the way I'm
using it. It costs about $200 a month.
They do have some cheaper plans, but in
my experience, they're way too limited.
I use Cloud Code on their $20 a month
plan, and I hit the limit in like 10
minutes. I used it on the $100 plan, and
I hit the limit in an hour.
Realistically, my recommendation is to
use the $200 plan.
So, when you subscribe to Claude Code,
you can choose between using the Claude
Sonnet 4 model or the Claude Opus for
model, or you can have it auto select
and try to use the best one for the
task. Personally, I just have everything
set to opus because I'm paying for the
max plan. And even using Opus for almost
every request, I rarely hit the limit on
the max plan, but I have heard people
say that Sonnet 4 is actually good and
sometimes even better than Opus in some
cases.
Why is this thing performing better than
Cursor Agent if Cursor agent is using
the exact same model? So, that was the
first question I had and I did a little
bit of research. I have no definitive
proof here. So, this is just my opinion.
My hypothesis is that cursor is super
optimized from a token usage standpoint
that it does a lot of things like
compression and not using the full
context window to try to save cost which
makes sense because at the scale that
cursor is operating at they have to do
whatever they can to try to get the
token usage down so that way as much as
possible can fit in the $20 a month
plan. I think that claude code is not
doing optimizations like this. I think
it is eating a ton of money. Someone
wrote a program you can run to actually
see how much tokens you consumed, how
much it would have cost if you were on
the API based pricing. Here's what my
usage looked like in a little over a
week. If this is accurate, I have used
over $3,000 and over a billion tokens in
a little over the week, which is
absolutely crazy. If that's accurate, I
think Cloud Code is losing Anthropic a
ton of money because I'm just paying a
flat $200. I think it's not as optimized
as Cursor and it's just consuming
tokens. And what that does is it
probably allows for better output. This
makes me really question how Enthropic
is doing this. They're probably doing
this to try to take more market share.
Anthropic has probably 1/100th the
number of users on Cloud Code than
Cursor does. So, I think that they can
sustain this a little bit longer. But,
if developers start picking up on this
and start using Cloud Code, who knows
how long this is going to last. I
probably just accelerated that timeline
by making this video, but I think
everyone's going to figure it out
eventually. So, I think it's worth
sharing with you guys.
Okay, so what are the downsides to it?
Number one, the cost is extremely high.
I think to use this effectively, you
have to be on the $200 a month plan,
which is just not affordable to most
developers. But if you can afford it, I
highly recommend trying it. Maybe I'll
do a whole separate video about coding
tools at different price points, but the
price point is probably the biggest
downside. The second downside, which I
already mentioned, is that there is no
checkpoint functionality like cursor
agent where you can just restore to a
specific point in the chat. You have to
do that manual workaround with git that
I'm doing, which kind of sucks, but I'm
kind of used to it, so it's not even
that big of a dealbreaker anymore. And
number three, it takes a very long time
to run. Some of the actions that I take
have taken over 30 minutes to run, which
really can be disruptive to flow. But
again, since you can in theory run sub
agents and run things in parallel, that
is a way to cut back the time. You can
also just open up multiple terminal
windows and use multiple instances of
clawed code at the same time, which I am
frequently doing.
So, who is this for? I think that if you
are a developer who does a lot of coding
and if you make apps and you make money
from your app, I think this is a
no-brainer at $200 a month because I am
getting substantially more value than
$200 a month. At least in my case. So, I
think if you do this stuff as a
professional and you make money from
software development, this is a really
good investment. I think if coding is
just a hobby or you're just getting
started, I actually recommend just
sticking with cursor and using that
instead. Again, there's nothing wrong
with cursor. It is still an incredible
tool. It's just that claude code has
been better in my experience. So that's
why I've switched to it right now.
Please share your experience below. And
if you have any tips on using Claude
Code or you found something even better,
please leave a comment down below. I'm
always looking for new tools and ways to
improve my workflow. But I hope you guys
found this interesting. If you like this
kind of content, check out my Instagram
and Tik Tok. I post almost every other
day about building productivity apps.
And obviously, if you like this content,
don't forget to subscribe. But thank you
guys so much for watching and I'll see
you guys in the next video.
[Music]