# Claude Code Is The Best AI Coding Agent

Source: https://www.youtube.com/watch?v=77snqcntze4

Cloud Code is the best programming agent
in my humble opinion. I've been using it
since it dropped. I actually was at the
Cloud Code conference and seeing the
announcement drop. I saw it drop live
and ever since then, I've been using it
every single day. And I wanted to give
you guys a short quick tutorial on how
to get started, how to use it, and what
I think about the programming agent
world right now as we speak. Cloud Code
has really shifted the way I look and
think about things and even how I use
these tools. Now to get started, it's
pretty simple. All you really have to do
is run this command npm install-g and
you run atanthropic-
ai/cloudcode. Now here's the thing. You
can use cloud code with any IDE. VS
Code, Jet Brains, Cursor, Windsurf, Zed.
It works with anything. Although with
Zed, there are some features I realized
weren't working properly, but I'm sure
it'll be fixed by the time this video
goes live. And literally all you do is
CD into your project directory and then
you type the command claude. Now in
terms of pricing, you can either
subscribe, it used to be just the max
plans, but now they've added cloud code
in the $17 a month plan, but you can
also use the API more as a pay as you go
type vibe. So whatever makes sense for
you, but at $17 a month, it's an easy
entry, great price point for you to
test. Now, I just want to dive in a
project and show you how I use Claude
Code. So I have a new terminal. I'm just
going to type in claude and then this
interface pops up. Now there's something
cool about cloud code where it has
context into which page you're in. So
right now I'm on page.tsx and it knows
that I'm in page.tsx. So if I ask tell
me what this page is doing it because it
knows what page I'm on, it's going to
extract the information. It's going to
look at the code from this page and tell
me exactly what's going on. So it says
this is the home landing page component.
It displays a centered hero section with
a title lock screen AI description text
and generating Apple passes for
communities. Two action buttons that
link to dashboard and dashboard/create a
hero image. This me this page serves as
a main entry point. So you get the idea.
Now what's cool is just like with any of
the IDE like cursor and windsurf I can
type an at and I can specify a specific
file. Like for example, I can do at
middleware explain what this file is
doing. So I can go to specific file and
ask. I can also tag specific files and
ask. So it tells me authentication
protection, invitation flow, public
routes, and route ma matching. Now where
does cloud code shine? Cloud code shines
in big code bases or already existing
code bases that you're not familiar
with. I can't tell you how fast it's
been for me to onboard onto new code
bases with cloud code. I'll just ask it.
explain to me the flow. How does this
page work? How does this component work?
Well, how does this app work? It can
help you onboard into code bases so much
faster. And I can see this for companies
and teams being valuable or even if
you're someone who's a contractor,
freelancer, or you're joining a new
company, definitely make sure you ask
for a cloud code subscription. So, I
actually have a bug on an application
I'm working on and I want to show you
how I'm going to fix this with cloud
code. So, I should be able, this is an
Apple Pass, I should be able to delete
this, but for some reason I can't. So,
what I'm going to do is I'm going to go
to cloud code and I'm going to go tag
the page because I know what route this
is in. This is in the slashdashboard
route. So, I'm going to do dashboard.
I'm going to do
dashboard/page.tsx. So, I'm going to say
in this page,
um, as an admin, I should be able to
delete passes, but for some reason, I
don't see the
deleting the delete button. Now,
non-admins should not be able to delete,
but as an admin, I should be able to
delete. Simple generic prompt basically
explaining the functionality I want. And
now you're going to see Claude code work
in action. Now, real quick, while it's
working, quick praise break. I could
call him. I could call him in the middle
of the
night. I could call him in the morning.
I could call him in the middle of the
night.
I could call him in the morning. I could
call him in the middle of the night.
And when I call him, he'll make
everything all
right. It does not matter
how Jesus promised he'll take care of
me. So, we see that again. This is a
true agent. It continues to iterate on
the task. Now it says the serverside
delete pass function is correctly using
check pass delete permission. Let me fix
the delete pass component to remove the
client side admin check since the server
function already handles permissions
properly. Okay. So it's asking me do I
want it to make this edit. I can say
yes. I can say yes and don't ask again.
Meaning just keep on reiterating. or if
I think it's going the wrong direction,
I could tell it no and tell it why. This
is why I love it. So, I'm going to click
yes. This makes sense to me. So, it's
making edits to the code. It'll show you
here also how many tokens are being
used. Now, it says now the delete button
will always be shown and the permissions
check is handled server side. So, let's
go back and yep, I can see the delete
button there and I can delete passes.
So, it fixed that bug for me. I told it
here that even though the server side
check works, I want the button to not
show the delete button to not show for
non-admins. So it said you're absolutely
right. The UI should be smart and
showing and hiding the delete button
based on the actual permissions. Let me
implement a proper solution. Now I took
Claude's um advice where it says
encourage deep thinking deeper thinking.
I I told it to think about it and you
can see it's starting to work and you
can see a diff view here meaning it's
showing you the code that it's written
and we can see the task that it's
implemented. So it's checked list all
passes function to understand the
current data structure. Now I'm actually
going to say yes and don't ask this
session. So I'm going to let it rip and
see if it actually works if it actually
builds this functionality out properly.
Make your
friends. Put your phone down. Put your
phone down.
[Music]
So, it says it is done. It wants to run
a build. I will just say yeah, I'll say
yes, run a build. Fine. It's cool with
me. We'll let it run a build. Unless you
see that it's last test is test and
commit changes and it actually wants to
commit the changes. So we'll let it do
that. So get add get commit. And this is
the commit message. Looks good to me.
And it wants to push these changes. Yes,
proceed. And as you can see here, the PR
has been made with the right
descriptions. I can review the code.
I'll just create this pull request real
quick. And what's awesome is again I
have uh code rabbit which also can
review this code and we're just living
in a time where using agents for your
workflow in whatever field makes sense
and yeah I've been having a good time
with cloud code. Now there's some other
common tasks that enthropic um suggest
um like for example we will we automated
git operations we made a code edit but
testing writing tests nobody likes
writing tests but we should write tests
maybe this is a good way for you to use
cloud code and it says encourage deeper
thinking for complex problems explicitly
ask cla to think more deeply right so
this is the first time that I've seen
true agentic coding and this is why
claude code has been my favorite
programming u agent I actually cancelled
my winds surf cursor or subscriptions. I
am strictly using uh claw code. And then
if I want to, let's say use the chat for
zed, I've been using zed right now. I
have an API key. I'll just pop the API
key and use that. And it's been a fun
time. And that's pretty much it for this
video. I hope you enjoyed. I hope you
give Cloud Code a spin. Let me know what
you think in the comments down below.
I'll see you in the next one. Peace.