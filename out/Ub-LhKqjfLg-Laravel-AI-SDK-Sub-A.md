What if your AI agent could just ask
another agent for help? Multi-agent
setups are everywhere right now. So,
instead of having this one giant agent,
you give each job to a focused
specialist and let them work together.
And the Level AI SDK just made this that
simple with sub-agents. And the trick is
elegant. A sub-agent is just an agent
you hand to another agent as a tool. The
parent decides when to delegate, gets
back the answer, and folds it into one
reply. Let's see what this looks like.
Here in this application, I have this
billing support agent. And before we can
talk about sub-agents, we need to talk a
little bit about what an agent is. An
agent is This is part of the Level AI
SDK. Think Think of it as a specific
assistant when working with AI, which is
Yeah, just have some specific targets
focused on some specific tasks, like in
this example is billing. Or it could be
about customer support, it could be
about sales, or anything else. And the
only thing different to just a prompt to
a specific AI model is that we have some
instructions here to tell it what it
does, and then we later we also have
tools here. So, in this case, we're
telling, "Hey, you're billing support
specialist, and use the invoice lookup
tool," which is a tool which we have
down here, look up invoices, which is a
tool which you can also create with the
Level AI SDK. And this helps us to
connect this agent to um this tool, and
this tool can look something up in the
database and give this back to this
agent, which is really cool. So, let's
also give this a try.
I have here this artisan command which I
created to
um What was it? Um support
chat, I believe. Yeah. Okay, this is a
little artisan I created for this demo.
We can pick here one of our agents.
Here, we have two. I'm going with
billing first. And then we have this
kind of conversation loop here inside
the terminal to show you what this can
do. So, um please show me
my last invoice for
and then I'm providing this email. And
we also have some output here in the
terminal, which shows you which agent is
being used and which tool. So, this was
a little bit too fast. So, yeah, we are
inside the agent. It's using the look up
invoices tool, and then we're back
inside the billing support agent. And
now we're getting this last invoice and
the information about that, which you
can see is working. Um the same, let's
try this now again, also works for the
technical support agent which we have
here. So, I get a 500 error when logging
in.
What could this be?
And now it should use another look up
tool here. Yeah, you've seen it
previously here. Let's go up here.
Yeah, this one. Look up technical angels
issues, another tool that also talks to
the database
where we have those stored, the typical
issues that we have in that application
here. And then we get some information
back about what this could be. Um
severity, status, and so on, which might
help the user. Okay, this is pretty
cool.
Back here, we can see we have those
agents here both in here, and we also
have our tools here, which is pretty
cool. And again, it's also a good idea
to separate those agents here because,
yeah, they have very specific things
that they need to do, and it gets a
little bit messy if you try to make one
agent that does everything and holds all
the tools here.
But there is still something that's very
interesting here in this case, which are
sub agents. So, let's imagine we still
want to have this one main agent here
for customer support, which takes all
the requests from the user, and then it
can delegate it to other agents like
this one here. So, let's try this
together.
We are creating a new agent, make agent,
and we call him this main support Asian
and we don't need structured output,
which you only need if you if you feed
the result directly
to the eye again, but we also get some
conversations back here.
Okay, let's go back to the application
and let's take a look at this here. So
this is now our main support Asian. This
should get all the first messages from
the user and then it should delegate it
to our other Asians here.
So this means first we also need to give
it some instructions so that this
conversation knows
how it should behave.
And here we are. You are the main
support Asian for our demo here.
Classify each customer request and
delegate and the
specialized work. So first is billing
invoices payment plan and so on and the
next is park errors login shovel and so
on.
Use the sub Asian or which we haven't
defined yet to respond concisely. So
this means it delegates everything to
the sub Asian and then the sub Asian can
do all the work thinking about having a
judgment about what's going on and then
we only get yeah, specific result back
that we can then use here.
So this means in order to make this
work, we need to create now those sub
Asian, which is now the cool part here.
We can do this right here inside our
tools where we normally would add just
only our tools, but now we can add our
technical support Asian here and we can
create our
um billing
support Asian here. Well, then we're
going to create a new
And fixing here the paint issues. All
right, cool. So why don't we just
provide the tools here and use here
those Asians here. So a good thumb of
rule here is whenever you need only
a specific tool, something that's been
done like get something from the
database without any judgment, then
you're using a tool. Like look in the
database, look for this issue, give me
back this issue. Whenever you need also
some judgment involved, then you would
grab for an agent here, which not only
gets the data from the database, but it
also analyzes, think about what to do
with this data, and then gives it back
to our main agent here, which is now in
this case.
So, the only thing left here, I have
this artisan command where I have
provided all the
uh agents that we want to talk to. I'm
just giving this a name, and now we're
adding our main support agent class. So,
I will also attach the repository for
this demo here. But yeah, this is just a
helper which you've seen in order that I
can talk to those agents here from my
terminal, and now we also have the
options to talk to the main one.
All right, let's try this again.
Mm, support chat here, and now I can
select the main one.
And now I can ask the same,
"Please
show me the last invoice for
Jane." Here we go, and now we should see
a little bit more happening in the
background.
And I'm waiting for the final result.
Okay, let's go up here.
So, we were first in the main agent here
where we have this prompt, then it was
switching to the billing support agent,
then inside that it was
using our tool here, then back to the
billing, and then we got back to the
main support agent here, where this one
now got the result from the billing
support one, and now we have the result
here, which now our main agent decides
how to provide this now to the user,
which is pretty cool. So, this means we
just have now a couple of agents here in
this application, the billing one, a
technical one, and the main one, and the
main one is now responsible to get the
first message from the user, and then it
can delegate it to the other agents that
we have here in this application, which
I think is a really good approach
because, yeah, again, think about that
separation of concerns. Every agent now
has some specific instruction. You don't
need to blow up the whole instructions
of your main support agent, and every
agent just has a specific task and is
best for this, and this keeps everything
very clean inside your application when
you work with the Llama AI SDK and with
our agents.
And that's sub agents in the Llama AI
SDK. One parent delegating to focus
specialist, each with its own
instruction and its own model. Quick
rule of thumb, reach for sub agents when
a subtask needs real judgment and not
just action. Otherwise, a single agent
with tools is still the right way to go.
If you want to dig deeper, check out the
multi-agent workflows guide in the docs,
[music] and if this helped, drop a
comment with what you built, and hit the
like and subscribe button, and see you
the next time. Bye.