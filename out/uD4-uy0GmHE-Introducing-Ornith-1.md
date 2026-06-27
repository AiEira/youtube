Okay, so just as news of GPT-5.6
has come out that the government is
going to be preventing people to use
this, open weights models keep chugging
along. And this brings me to the topic
of today's video, Ornith 1.0, which is a
family of models from Deep Reinforce.
And I guess the big tease here is that
things have been moving along where
we've had sort of one track B models and
one track B harnesses. And what Ornith
is proposing is why not have a model
that writes its own harness, or at least
has the ability to write its own
harness. Therefore, if you've got a
particular use case that needs one kind
of harness, it can write that on the fly
and then be able to use that to actually
get the result that you're trying to
get. And this is exactly what the Ornith
family of models are trying to do. They
actually call this self-scaffolding LLMs
for agentic coding. Now, the area that
they're focusing on is agentic coding in
here. I think the lessons can probably
apply to other domains as well, but it
does seem the whole topic of agentic
coding is where the money is at the
moment and where a lot of people are
trying to make the most innovations.
Which makes sense with everybody using
things like Claude Code, Codex, and all
the other agentic coding tools that are
out there. So, that brings us to what is
actually in Ornith 1.0, their family of
models. Well, this is four models that
are not new pre-trains or anything.
These are basically fine-tunes or sort
of more mid-training and post-training
on four separate models that come from
the Qwen 3.5 family and the Gemma 4
family. So, we've got a 9B model, which
is Qwen 3.5. We've got the 31B, which
comes from the Gemma 4 family. And then
we've got a 35B MoE and a 397B
MoE, both from the Qwen 3.5 family. Now,
the cool thing in here is that they've
released all of the models, unlike some
of the things we've looked at recently
where they've held back the biggest and
best model. Here, we've got all of the
models available, so you can try it out
whether you're just looking out to try
the 9B small model, whether you want to
try the 35B MOE, or whether you want to
go really big for the 397B.
But, the key thing that sets this family
apart is that these models are learning
to generate both sort of solutions roll
out, so agentic trajectories, and
task-specific harnesses that guide those
roll outs. So, their whole goal is by
optimizing both that sort of scaffold
{slash} harness and the solution that
the model is then going to basically
generate better solutions out. And if we
just quickly look at the benchmarks, I'm
not going to harp on about these, but
certainly looking at their really big
model here, we can see that it's
outperforming a lot of other models,
including the Quen 3.7 max, the mini max
model, and often is competitive with the
Claude Opus models. If we do the same
thing and look at Even the smaller ones
are doing very well against models their
own size. And that's for the 35B MOE and
even down to the 9B. So, the 9B is
certainly something you should consider
if you're looking to run a local coding
model and you can't run something as big
as the 35B or or the Gemma 431, etc.,
their 9B model is doing really well here
compared to those other models that are
often even three times as big as them.
But, what's far more interesting than
the benchmarks for me is what actually
makes this special. And this goes to the
heart of sort of what they're getting at
here is that Up until now, most of the
time people thought about agent
harnesses as being things that are
designed by humans. So, what Oracles
actually does here is they treat that as
a learnable object. And the whole idea
is that just as the model's going to
learn to be able to get good results, it
should also learn to create better
scaffolds or better harnesses for
creating those good results. You could
even think about it as their model
learning to do context engineering
instead of you having to write that by
hand. And that idea here of how do you
actually train a model or sort of
mid-train and post-train a model to be
able to do this without it all falling
apart is the key thing to me about this
project. And this really comes down to
this sort of two-stage IRL process that
they've got here. So, they basically
propose a task, and then they condition
on that task and a scaffold previously
used for it, and then the model will
first propose a new sort of refined
version of that scaffold or that's
harness, and then conditioning on that
new harness, it will then basically
propose the rollout which is going to
get us to the result that we want. Now,
then what they do is they take that
rollout and because they'll have
multiple rollouts there, and they will
then basically use that as a reward
signal to update the model for both
generating the scaffold and generating
the rollout here. Ideally, what's going
on here are those reward signals, and
this is coming from using GRPO here, and
I'll talk about how they're doing the
verification in a minute, but that
allows them to basically update the
weights of the model to get better at
building a scaffold and then better at
using that scaffold to actually generate
good results out. Now, currently,
they're focused on doing all of this in
the domain of agentic coding, so it kind
of makes sense, and based on their
benchmarks, it seems to be working for
that. But, you could imagine this being
used for other kinds of tasks. Now,
obviously, the challenge that you've got
is can that reward signal be something
that you can measure with GRPO, is it
something that's verifiable, etc. And
the thing you should be thinking about
as you're sort of looking at this is,
well, if the model is determining
basically how the harness works and the
actual rollout, why doesn't it just
cheat and build a harness that just
takes a shortcut to get to the right
answer? And obviously, this is something
that they've thought about a lot, too.
They actually address this in how they
deal with reward hacking. So, remember
reward hacking is where if you've got
some kind of LLM as a judge or something
like that, the model just learns to do
tweaks that are perhaps not exactly what
you want, but that are going to get the
best reward out of that model. And in
the early days of RLHF and RLAIF, etc.,
you would find that the sort of
generator models would generate all
these kind of weird ways to get the
reward model to just give a high signal
back. And that could just be repeating
certain tokens, doing stuff things that
as humans we would clearly see as being
wrong, but because the reward models
were perhaps not as good back then, they
could be tricked quite easily. Now, that
said, even though the reward models
nowadays are better, there's no
guarantee that that alone is going to
give you the best reward signal to
actually update your model. So, they
talk about here of basically defending
against this in three layers. So, the
first one is the actual environment and
sort of tools and I guess basically
everything that's going on in the
sandbox that the scaffolding is going to
run in. So, all of those things are
immutable. They can't be changed by the
model. So, the model can't set up the
environment to actually do a shortcut to
sort of win kind of thing. Secondly,
they've got a deterministic monitor
here, which is kind of cool, right? That
what they've got is something that's
basically watching what does the
scaffolding actually try to do? Does it
try and do anything like modify
verification scripts, use any sort of
unsanctioned tools, try to use anything
that's out of the sandbox that it's
allowed to play in. And the moment that
it does that, it basically gets
penalized for doing that. And the third
thing that they have is an LM as a judge
that can veto on top of any of the other
stuff. So, even if it passes the early
stages and stuff like that, if the LM as
a judge also says no, this has been
achieved in some way that perhaps wasn't
allowed, it can then veto the whole
verifier that the GRPO was using, etc.
So, overall, this is a really
interesting idea here of can a model
then actually sort of code what it needs
as a harness on the fly. And we've seen
the idea of models actually writing code
that they can then use be around for
quite a while. So, this is the PAL
paper. This is from It was late 2022 was
the first version of it. This published
version is January 2023. And what was so
cool about this was that it basically
proposed that why doesn't the model just
write Python to do things like math and
things like that and then run that
Python and bring that back into the
model. So, that kind of idea is actually
quite old. But getting it to write a
whole scaffold shows that one, not only
have we come so far in the models that
the models have gotten so good at this,
but this could be the way forward that
as the models get more intelligent, we
don't want to basically get involved as
humans much at all. We just want to
leave it to the model to write what it
needs to get the result that we want
out. So, let's have a look at the model,
see what the actual outputs look like,
and get a sense of how this is all
coming together. All right, so if I come
in here, I'm using my testing suite in
here. You can see we've got the model.
I'm using the 35B MLE here. If I give it
something like this, right? So, just
starting off with some sort of general
things. Draw pelican. So, the whole
pelican SVG test, it draws a pretty nice
pelican in here, right? So, you can see
that like this is straightaway getting a
pretty good result for the pelican,
which is kind of be expected. I'm
guessing that I can't remember testing
the Quen 3.5 model on this, but that
does quite well. If we give it a rag
question, you can see we're getting it
where it's writing up a lot of sort of
reasoning thinking tokens in here. It's
basically gone through and looked at the
different stuff in there, but it hasn't
really written any code or anything for
this. It's just worked out, "Okay, this
is what should be the answer." And then
it comes back and gives us answers in
there. Again, still pretty impressive.
And it does that for quite a number of
the other sort of tasks as well. If we
give it something that where we say,
"Create a harness to get the weather
with a 5-day forecast." And we run this.
By the way, the computer here is
sponsored by Dell. I'm actually running
this on the Dell Pro Max with an RTX
6000 Pro here. So, I'm getting very good
speeds that you can see for the model.
I'm able to run both the 16-bit models
and also quantized models here. This one
is actually a quantized version that
we're running through a llama. Uh you
can see for some of the other ones, I'll
run them through VLM directly in here.
Anyway, if we come in here and look at
the thinking process, we can see that it
understands the goal of create a
harness. And it understands that it's
going to need to handle all the
different things that the harness does.
So, this is what is kind of unique with
this model. It then basically starts to
design a solution. We're getting very
nice long chain of thought here, which
is very clearly related to the task at
hand, going through this. And then it
starts to draft the code. In this case
it's done 1,600 tokens in there. If we
come in here, we can see we've got it
basically deciding it needed to have the
request library. It then basically
creates the weather harness. The weather
harness is going to be for 5-day
forecast in here. We can see that it's
decided how it's going to handle a bunch
of things for this harness and to
basically give us some graphical
displays, etc. And in this case it's
telling us, "Okay, we need an open
weather API key here." And it shows us
what some of the outputs should be like,
etc. Okay, if I change it to basically
say, "Right, we don't have any API
keys." Let's see, do we get something
now like an API which doesn't need an
API key in here. So, it's still
generating a lot of thinking tokens. My
guess is that the thinking tokens going
to be very similar. Although, we see the
implicit need now is find a free no API
required weather source. It's gone and
generated a lot more thinking tokens as
it's gone through this. And it's come up
with the result of using the open meteo
API, which is this API here. Sure
enough, doesn't require a sign-up in
here. So, it's then basically rewritten
the script to match that API. So, we can
see we've got these codes here, weather
interpretation codes, and it will
convert them to emojis and to a sort of
short description going through this.
Then it's going to take coordinates as
GPS coordinates. It's actually got the
API in there. It looks like it's handled
all of that very well, which is really
good cuz it understood the requirements
that I don't have any API keys and had
to basically do it without doing the
API, etc. And you can see now if we ask
it something like create a harness to
get the latest AI news from Twitter.
Let's see what it's going to come up
with. It is really nice that when the
tokens are this fast, you don't mind
having a few thousand thinking tokens
going through this. And we can see
coming in this, okay, get the latest AI
news from Twitter's API has changed
significantly. It's doing quite well at
understanding that. It's then got code
for it dealing with the actual sort of
main Twitter API. Okay, what if I change
this to telling it I don't have any API,
so find a solution that doesn't need
one. Are we going to get this in the
thing? Okay, no API keys allowed. Need a
solution that bypasses this requirement.
So, you can see that the chain of
thought has kind of been trained for
very specific things. First, understand
the user request. So, this is a common
thing that it is in the sort of hidden
chain of thought for a lot of the
proprietary models. It's got the
constraints there. It's got identify key
challenges, constraints, explore
alternative approaches. Let's see after
3,200 tokens of that, what did it come
back with? It's come back with, okay, a
list of accounts that it should follow
for this. And it's basically just going
to use requests to try and scrape it
directly in here. I'm not sure how
successful that would be. Wouldn't
surprise me that that would get blocked
very quickly. But we can see that the
logic in the harness is sound for what
it's trying to do in here. Don't forget
this is just one shotting it as well.
You could set this up to basically keep
passing results in. And you could also
set it up to actually take the code out
and automatically run it and stuff like
that. And so, you can see that the other
thing too is it actually ends on with
each one basically asking, do we want to
have some kind of simple Gradio or
Streamlit UI, etc. Okay, so I've come
over to my chat sort of testing where
we've put in just a simple system
prompt. It's gone through stuff. It
looks like it's found a little bit of a
different solution this time. But I want
you to see that like that it's now gone
and rendered this nicely. You can see
we're now in a chat thing where if I
basically ask it at the end of that,
"Can you build a Gradio interface?"
Interestingly, this time the thinking
was very quick. So, it understood that
it it created the sort of, you know,
harness already and that now this was
basically just going to structure out a
plan to do the rest of the Gradio
element of it in here. So, it's not sort
of redoing the whole Twitter thing,
which is good. We can see that looks
like it's made the Gradio app pretty
well and pretty quickly in there. So,
overall I would say that this is
definitely a project that's worth
checking out. Try out the other models.
I've gone for the 35B N O E, but you
could certainly play with this with the
smaller 9B model, which is based on the
Qwen 3.5 series as well. And let me know
in the comments what kind of results you
get with this. I don't think this is
going to change my daily workhorse for
doing coding kind of tasks. I do think
if you wanted to do local coding and you
don't have access to a big GPU, this is
something you could certainly check out.
Anyway, thanks to Dell for sponsoring
the compute in here. As always, if you
found the video useful, please click
like and subscribe and I will talk to
you in the next video. Bye for now.