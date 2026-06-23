# Game Programming Patterns for Godot – Inacio Schweller – GodotCon 2026

> 來源：[YouTube](https://www.youtube.com/watch?v=TjlstMYREls)
> 長度：約 32 分鐘
> 語言：英文
> 整理：AiEira

---

<!-- BLOG_REWRITE_PLACEHOLDER: LLM will insert rewritten blog here -->

---

## 全文逐字稿

<details>
<summary>展開逐字稿（共 826 片段）</summary>

Hello.

Hey,

I am very nervous, but it will calm down

in the middle. So, yeah. Thank you all

for being here.

This is going to be super technical and

I'm not going to apologize in advance.

It's going to be a lot of code. There's

like 85 slides of code. So,

yeah. So, let's let's get to it.

Oh my god.

Why did you do that? All right. So, game

programming patterns for Godot.

Uh first of all, who am I? Because

nobody knows who I am. Um I started

studying mathematics. I wanted to be a

teacher. Uh then back in Brazil, I did 2

and 1/2 years of like math bachelor's.

And then I went to like try to teach.

You have to do like an internship. Then

I gave up because it's really hard. And

kids I just can't. Then I got a job as a

dev. Then I went to study art for fun.

Actually, take this off. Yeah. Uh yeah,

so and then as also like

like I said, I was working as a dev and

doing things as a dev and developing my

projects, getting paid, and

uh mainly it's a combination of those

things. I also like developed small

games in the past like this game that

won a game jam the Godot Wild Jam 21

like couple years ago.

Uh and also this like a very like simple

game and yeah. Anyways,

uh I'm working right now on a game

called Tiny Drift and I'm going to use

the code from the game.

Um yeah, it's going to be my first

commercial release. It's coming out in

October uh this year. So, I'm doing like

as a

solo Swiss Army knife developer, music,

art, programming, everything. And I

really love it. Uh yeah.

All right, agenda. So, why do we need

patterns? And I'm going to show you the

code. So, um,

why do we need patterns?

So, I believe that good code is code

that ships. I really believe in that.

That being said, I'm going to use my own

definition uh, as a back-end developer

for 16 years at the moment. Uh, for me

good code is something that is

maintainable,

that's also readable, and most

importantly, testable, right? You want

to ensure that whatever you're writing,

you can test and you can

kind of like predict the outcome of what

you're doing. Cool.

Um, I'm also going to mention

domain-driven design, and I'm not going

to apologize for doing this. And if you

don't know what it is, just ask me

questions after. It's something very

old. There are books about it. It's kind

of like standard in back-end systems.

And yeah, mainly also a lot of games use

it, but I was very surprised that not a

lot of people talk about this publicly.

Um, so yeah, if you have questions, if

you never heard about this term is the

first time, just reach out and yeah, we

can talk about it. But I'm not going to

explain too much about it. It's just

that I'm taking concepts from from it,

and being very like transparent about it

that I didn't invent it anything here.

Uh, the problem. So,

back to my game. Uh, I have these, you

know, enemies flying around, and they

have uh,

characteristics and stuff. And at some

point, um, yeah, I had this big object

called refs. It was an auto-loaded, like

a singleton object that has like a enum.

For some reason I did this, I don't

remember why. It was a long time ago.

And I also was preloading all the enemy

scenes. And I was also on the same file

keeping like the weight, you know, like

if I want to spawn them in the screen

and find like a, you know, which

chance of them spawning was also kind of

holding them in a different dictionary,

right? So, it's a big mess. Like it was

auto-loaded, it was referenced all

around my code.

It was It worked, you know, the first

version worked really well, but if I I

couldn't really remember why things were

done this way at some point. So, I

thought, "Okay, I need to change this."

So, I'm going to talk about a little bit

of the solutions.

Excuse me. And we're going to refactor

the code together. We're going to

discuss it. And we're going to get to

something that I think it's really

mind-blowing, in my opinion,

about things you can do with GDScript

that is not very

publicly spoken about.

So, let's talk about data data data

data. So, let's initialize data. So, if

you remember a few slides, I had this

thing here, right? So, I was preloading

a bunch of scenes. And this was a bit

messy for me. So, first step for me was

to initialize and get a list of things.

So, maybe some of you are familiar with

this pattern. I'm going to also give a

disclaimer about it. There is a proposal

already on Godot about this. So, maybe

gets incorporated or not. It's called

lazy loading.

So, basically, you have a cache and then

you want to compute a list of things.

You call it once, and then you save it

on a cache, and then you don't have to

compute it again. That's it, right? For

certain things in games, it makes sense

to lazy load. For certain things, it

makes sense to eager load. I'm not going

to go deep into that because that's more

performance things. But, yeah. For me,

it was important to build something like

this. So, basically, I came up with a

little file that I call enemy repo. I'm

going to talk about this in a moment.

That I can, you know, save the scenes

and I can scan the scenes from the file

system. That's very simple, actually. A

lot of people do that already, but that

was the first step for me, so I could

remove all the preload from the

reference files.

Uh cool.

That's the proposal, like I said. So,

it's Yeah, but I'm not sure if it's

going to be incorporated or not, but it

would be cool. I mean, it's very little

boilerplate anyways, but yeah.

Uh the data, right? So, I I had the

scene files. Um they were like repeat

repeating a lot of information about the

enemies. So, very basic stuff. I created

a resource with a class name, and I

created a bunch of resources, right? So,

that's second step. Very standard so

far, nothing brilliant.

And a bunch of information of the

enemies, nothing really big. Um yeah.

And the most important thing starts from

now. So, now we have the data we

initialize, we read it from the file

from the file system. We want to access

it, and we want to read it through the

code

um instead of reading from a singleton

or an autoload. And by the way, I'm not

saying the autoloads are bad, right? But

they start charging you rent at some

point, and that's a problem. They are

charging my code rent, and I didn't like

that. So, uh I got the same structure

that I just showed, and I create

something called enemy repo. Repo is a

short word for repository. So, I have a

bunch of functions. I'm going to talk

about them.

I have uh yeah, something called a

getter, basically, uh by ID, which is

the lazy getter that I just said. And it

looks for the cache. If it's empty If it

If it's empty, populate it. If not,

just, you know, returns the cache. Very

simple.

Um then I get by ID. So, I pass an ID of

an enemy, which I'm using as a string

name. It's No, it's not amazing, but it

works for me. And I can just go to the

dictionary and return that enemy. Very

simple, right? And I have this enemy

definition which I just showed in a

moment, like a few slides ago. I also

have a function all that I can return

all of them. So, it's a dictionary. I

can just do by ID that values.

So, it goes to the getter again, right?

And then gets the cache. If it's not,

just creates and then get me all the

enemies available. So, that's already

pretty cool and I don't see like almost

anyone doing this or talking about this.

So, that's a step one.

Also, something that it's important to

keep in mind. There is a function in

this file called scan. We keep it for

later. But if you can see, it just reads

the file system, right? Just looks for

it and initializes and that's very

simple, right? Returns a dictionary.

But we're going to talk about it in a

moment.

So, this is the repository.

Repository, it's an abstraction over

persistence storage that hides data

access details by pretending all data is

in memory. That's really important

definition. That's very nerdy. I'm

sorry. And that comes from domain-driven

design from Eric Evans. There's a book

written in 2003 and it's pretty much a

standard for big Yeah, enterprise

systems or even small stuff.

Let's see this in action now, right? So,

I have a spawner class in my level I had

I don't have it anymore. So, we can see

here that I go to the singleton, to the

global to get you know, array to type. I

also to kind of create like a

placeholder object. Then I want to do

the weighted spawning, you know, like

the to calculate the chance and then I

also get the references. I read the

dictionary that I showed a few slides

ago and then I return something from the

refs. So, I'm like it's a mess,

basically, right? If the singleton it's,

you know, cute free or something, I just

it's it's a mess and I don't know what

happened.

Um then I refactor it and it looks

bigger and I'll explain why in a moment,

but it's way better.

Um so, very simple first step, I added

the enemy repo, the class that I just

showed, as a dependency, right? And you

don't need to do it this way. I did it

this way because I wanted to test in the

editor. I still have it and it's very

convenient for me, but we're going to

explore different ways to do it in a

moment.

And and then I got to created a function

that's called pick enemy that receives a

list of enemies that are couple and

returns an enemy, very simple, right?

So, the biggest difference here that I

have references everywhere and now I

just take an argument and I

give back another argument that is from

the same type. So, I'm respecting a lot

of principles and I'm using what I

built, the the repo, to pick and

refactor my code and access the data

that I'm reading on disk. So, that's

already very, I'll say very good step

that you can do in your code and

I would say that most of the time people

do this, which is not, like I said, not

necessarily bad, but once it's,

especially if you want to test your

code, this is way better and we're going

to talk about this in a moment.

Uh and I I of course I

like the the code the calculus the way

it's not important, so that's why it's

darkened a little bit.

Um now the bread and butter, which is

the actually actually really fun stuff.

So, let's say for some reason you want

to load a JSON file, right? Instead of

your T-Rex or whatever or there's a talk

about YAML earlier, let's say we're

going to use YAML for some reason,

right? I don't know, I also like YAML.

Uh but in this example, let's say you

have a enemies.json file. Now, you

create a huge file called which I did

called enemy repo JSON. So, I'm

basically copying the same structure

that I just created and instead of

reading from the file system from the

resource files, I'm reading from my JSON

files, right? And I'm serializing data

back to Godot, which is a very hard

process to do by hand. I wouldn't

necessarily recommend and it can

actually give a lot of problems

disclaimer. But, if you're comfortable

doing it, right? It works for me.

Uh so, let's say now you you load your

enemies from a JSON, not from the

resource file. What is the cool thing

here is that because we're using this

extension,

the repo the the the class that spawns

the enemy has no idea that you're

loading your enemies from somewhere

else, right? That's first step.

If you're still using refs.mobs or

whatever or a singleton and then you

start loading JSON there, that would

leak that implementation detail would

leak to everywhere you are you're

referencing

um the those that data. But now because

you are abstracted and encapsulated in a

single class called repository, you can

pretty much switch and have like I don't

know any memory. You can test it, right?

And we're going to I'm going to show you

how how it's done later. So, that's like

really cool. Every implementation that

you follow this and you just inject the

dependency the repository, you can

pretty much change how you load the data

on the background without paying any

cost later and the code your code

doesn't know and then you can test it in

fully isolation.

So, let's take this one step further.

So, let's say now you want to create a

enemy source. So, I found that that I

was repeating a lot of code already and

I created this base class called enemy

source and it has just a simple function

called load all and returns a list of

enemies, pretty much, right? A list of

data. Uh

then I went

there and then I was like, "Okay, I have

now the resource enemies and I can

extend that class

and create a function that actually

reads from the from the from the

directory, right? So, I can also use the

the editor to help me there to change

the directory, for instance. Let's say I

want to have a

um drops resource instead of enemies,

right? It can be a boss resource. It can

be so many different things inside the

game.

Then I can also have a JSON one and I

can also use the export editor

variables to, you know, point to a JSON

in the in the data folder and serialize

this back to the to the to the game,

right? And that's really cool because

the repository code

it stays the same. It has no idea. You

can You just need to inject the source.

And then you can have many different

sources from this. You can have JSON,

you can have YAML, you can have in

memory if you're using GD Unity, you can

use the same abstraction in class that

you're using in game to test your code.

You only have to change the source and

that's very simple. The implementations

are the same. You have a init because

we're kind of doing like a lightweight

dependency injection here.

And basically you have this function

called load all that you can see it was

in the enemy source, right? You just

have to extend and create new

implementations of the class.

Um

cool.

Now,

the cool thing here is that this allows

me to have the same functionality. So, I

change a little bit implementation and I

can just do a like a lightweight

dependency injection. So, I can

instantiate a new repository and pass a

resource that's also a class, ref

counted, as new and then I can have the

enemies anywhere. It doesn't matter,

right? They're lazy loaded, so it's very

simple to use that.

I can also have modding, you know, maybe

someone you wants to use JSON for some

reason. Maybe people want to mod my

game. That would be amazing.

I can also test my game. It doesn't

matter, right? I can use the same

implementation and I can feed another

like in-memory enemy source, which

doesn't exist yet, but I maybe will

create it because it makes a lot of

sense for me and I can pass just fake

data to it because I just want to test.

Um cool. So, repository kind of answers

how to find me the thing. So, how do I

get this enemy? But the cool thing that

I also did is I I wanted to find enemies

that has certain characteristics, right?

And I I I wanted to answer this

question.

So,

um I at some point I had things like

this in my repository class. So, I want

to have all the boss enemies

for, you know, enemies with specific

tags or characteristics that are inside

the definition of the of the enemy

object. And that can get really messy.

You can like start adding methods and a

lot of games do that, actually. That's a

very common pattern.

So, enter the specification.

So, specification is also a

domain-driven design concept that it

encapsulate a yes-no question about a

domain object, which in this case are

the enemies of the game,

and encapsulate this inside its own

class, and that's really important. And

that's going to get really technical.

I'm sorry.

So,

I have this a spec file

and it's a class, very simple, right? It

has a bunch of functions and it has a

function called matches, and or and not.

And it also has extensions to itself.

So, there is a class N spec that extends

this spec and re-implements

a function that matches. And if you read

the code, it's pretty much like a

closure that says, "Okay, does this item

matches this other item?" If yes,

returns if yes or, you know, it's very

simple, right? And so, it's not a lot of

it sounds like a lot, but it's not a

lot. Um and that allows me to do things

like this.

Actually, to create a class that is

called enemy specs, but it could be

anything uh like an item or anything

that you can have in a game and have

things like this. For instance, a class

hashtag that extends the spec

and then it looks for the inside the

enemy definition if that enemy that data

has the specific tag I'm looking for. Uh

I can look for which is the minimum wave

in my game that the enemy can be

spawned. So, you can just write a little

class that extends the spec and ask

these questions, right? The

implementation is very simple. And or

you can also check if the enemy is a

boss. Very simple. Uh and then you can

create this and then you can test this

in isolation again.

Which gets to the point that uh if you

go back to the repository you can

implement a little function called find

here.

And if you read it, it receives a

specification that we just talked about

and returns a list of enemies. And then

again, very simple, go to the

dictionary, get the values, do a filter

because it's an array, and then you can

pass this back. matches inside because

it's a closure and you wrote these

callables in the other class, and then

it's just going to return the list of

enemies that

fulfill the criteria that you want. And

then you get into something like this,

which is really cool.

So, you can find, I don't know, like I

want to find everything that I can spawn

in wave five of the game. So, I can just

write like a enemies, that's the

repository, I initialize it prior and

then I can run find on it. Um that's the

the that's the function I just showed.

And you can have the specs, so like mean

wave, so wave five, and it's also not a

boss.

Right? Or I can find I can go crazy and

say that I want the fire vulnerable

airborne enemies. Whatever this means,

you can

also again do a find do all the specs in

line and you can pass them you can chain

the methods, right? You can do this in

GDScript. That's um

method chaining. It's a functionality

that many more modern and also old

programming languages have it.

Um and then again, you get the results.

Or you want to I don't know, maybe you

have elite mobs on your game and then

you want for some reason

um in certain wave in certain moment of

the game in spa spa the yeah, the elite

mobs. That's That can be done very

simple, right? And uh the repository is

where the things live. Oops, sorry. So,

the repository is where the things live.

And

I understand that for I mean I'm not

coming from the game development

background, so those things come very

natural for me. I prefer to go this this

route.

And

>> [snorts]

>> but if I think about data, I want the

easiest way to read it, right? That's

how that's why I built these

abstractions. So, if you want to think

about what is a repository is where

things live. Also a good pointer on this

as well is that

if you come from the database world, if

you work with databases in the past, if

you knew knows the concept of ORMs,

object relational mapping,

this is exactly what a ORM implements.

This thing here. Uh sorry.

These things here. So, it gives you

uh

type of language that abstracts how you

find your data, so you don't have to

write

the let's say low-level code. So, that's

all what like object-relational mapping

libraries do for you, and they are very

popular in the back end world, actually.

That's You don't start a project with a

database without it, actually, because

it's super hard to do it on your own.

So, you don't want to do this.

Um yeah. And going back here, so yeah,

repository reference leave. This

specification is

how you ask about them. So, what are the

criteria, right? And if you reflect

about if you're also like coming from

the uh sub regular software development,

you want to do a SQL query, is the same

concept, right? You you you ask certain

characteristics on the query. And then

you give certain parameters, and that's

exactly the same format.

Uh you don't have to use it to to use

those together. Absolutely not. You can

use one or the other. They are

composable. They are interchangeable.

You can pretty much, yeah, choose

whatever is uh you know, also you don't

need to use either this. I went like a

good amount of time without using

anything until I found out that, oh my

god, it's too much.

And I It's a very small game.

Um think of like uh tiny query language

that you're building for yourself that

is testable, and it's like abstraction

on top of something that Godot offers

you already, right? If think about Godot

and Godot resources and the file system,

it's kind of like a database already,

right? There is a lot of functionality

for you, but like I think most of the

people don't really see data like that.

Um but if you build it in the way you

can extend and just describe to

yourself, okay, I want to

find items, I want to find enemies, and

you you can actually make this available

to every other layer of your game,

right? It's a repository lazy loaded, so

you can just use UI for this for that.

You can

actually spawn the physics enemies in

the code, right? Or in the in the level.

So, you can really abstract things with

this implementations.

And yeah, and then if I would like to

have like a

takeaway from this talk, right? Uh don't

ditch the auto load. It's actually

really nice. You have to have

singletons. They're really really cool,

you know? Yeah, I think we overuse a

little bit, but all good, you know? We

still have

uh time to be saved. Uh but reach for it

when the auto load kind of starts

charging rent for your code, you know?

That once you feel like

hey, actually I cannot progress here. I

don't know why why I want to test my

game or there's this bug that's

happening on the play play tests. Uh

think about patterns. Think about what

can you abstract and make your life

easier, and try to critically think when

to implement something instead of just

doing because I told you to do it. Even

though it's very easy, you should do it.

I recommend. Um

and that being said, thank you so much.

Yeah.

And those are some links for my socials.

I figured out that I had to add this on

the last slide and I didn't add it until

today. So, if you want to wishlist my

game or message me on socials, it's all

there. Have fun. Uh

yeah, I don't know if we have time for

questions. Yeah, we have 5 minutes, so

we have certain questions, and feel

free.

If you have questions, don't make them

really hard, please.

Ooh, Eric is really working hard.

>> Hey.

>> Hello.

>> nice solution like to not have

auto load singletons. However, we need

to access those repositories from

multiple different places in the game,

right? So, how do you solve it? Like you

create separate repositories, but then

how do you think to have like the same

source for everyone? Or do you have some

global after all?

>> I mean, I I like I said, I don't I don't

tell people to ditch globals for auto

loads, right? Absolutely not. In my

case, I load them as a node. That's it,

right? I load the repositories as a

node. And that's why I was using

editor exports everywhere because I can

easily swap nodes and data. That's how I

do it. But there are probably many

different ways of doing it. Um

yeah. Like at the at the moment for my

game, I don't think too much about the

performance in of accessing the data

even

uh accessing at some point again, you

know, if I have to because I it's not a

price I pay. I pay more for the

productivity of like being able to

develop and test, but it's a very valid

question, and that's how I do it.

At the moment, I don't know if it's the

best way of doing it. It's the way I

found how to do it with Godot. So, I

just have like an

a node in the root scene, right? That

never goes away after it's lazy loaded.

>> Okay, makes sense. Thanks.

>> There are like a few questions here.

More?

>> Hi.

Uh obviously it's going to get more and

more complicated as you add more

parameters. Did you ever consider

something like Godot's SQLite extension?

>> I have no idea what you're talking

about. Maybe I should research it.

>> [laughter]

>> But it sounds really cool, I guess. I

mean, I'm also I'm

user, so probably something I would be

benefit especially I can imagine this

kind of system being very good for card

games for instance which you have a huge

amount of resources and maybe you don't

want to do everything in the editor you

know stuff like this and then you just

build this realization and use the repo

to load. But it makes a lot of sense

right you can probably yeah I'm going to

research it. I had no idea it existed.

Do we Oh cool. One more.

Oh you sound like you're going to make

it hard for me now.

>> First of all compliments for sitting in

front of a room of game developers and

talking about the architecture.

>> Oh my god yeah.

>> [laughter]

>> I thought about this actually I was like

what the hell I'm doing.

>> Very brave. I really like the style.

My question is you talked about

testability when you started off. Do you

unit test your games?

>> Absolutely.

>> Awesome. Can you tell me more about

that? How do you do that?

>> Um I mean wait. So this

uh here like I literally use this

functions on my unit test.

And I can actually if you add me on

Discord I can send you my code of the

test like I don't mind

um really. And after my game is out

please decompile my game and check

everything.

Um like this is how I test actually here

like I use this.

Like something like this I just don't

don't use the in memory any source but I

that's the structure I use on my test so

like I run the cases and before running

the cases I create a new repo with a

data. That's it. I use this actually.

But you should unit test your code is

very simple and very easy.

Say it again.

Yeah true. Well yeah.

>> More questions?

Go for it, Eric. You're doing great.

>> Thank you for your talk. I had a lot of

fun. Um I've had the several of the

issues you describe and you fix and I

kind of fix them the same way you do.

But no one can read them sometimes, not

because of the um

the way I define them. It's mostly

about, you know, we don't do it like

this or why are you doing it? And I have

uh I know uh I taught Haskell for quite

a while, so I know a lot of functional

programming and I find that it's very

useful in a lot of like data managing

cases. I was wondering if you see Godot

implementing more functional programming

in like there's lambda functions, but

more niche and if you find that there

would be an audience which we can teach

to use.

>> Yeah, that's a absolutely great

question. Um

Um uh there's first of all, it's a long

time since I contributed to the source

code. It was like Godot um was still

Godot 2, so really I don't touch the the

source code or contribute, so I don't

know exactly the direction things are

taking at the moment. Um I personally

would appreciate more of it, for sure. I

mainly work with Golang and Rust. Um and

yeah, like uh in Golang, it's not

necessarily functional paradigm, but you

can do it, of course. Um I do think that

things like chaining methods, you know,

currying and other things could be

really cool to be implemented in

GDScript and it's

it the ergonomics are very loose in a

way in GDScript that allows you to do

it, you know? So, that's kind of nice.

It allows me to do stuff like, you know,

like this, you know, which is looks

weird, but actually the ergonomics is

it's actually kind of nice, you know? It

looks weird like reading here, but it

works really nice. So, I think

I I think there's an audience because

data-driven games, they are very they

can actually get a lot of out of these

systems now things written this way then

you just declare the data and then the

way you access it is very declarative,

right? Um, but you also have imperative

methods and stuff. So, I would really

appreciate until it happens, I would

just created my own, I guess.

Stuff like this. And also if you like I

worked a lot of like JavaScript

libraries in the past, they also

implemented chaining methods and I took

a lot of these ideas from there too, by

the way. Because I used to work a lot

with it. So, I basically just look at

those, you know, um, ergonomics, those

methods, the constructors like how can I

do it similarly, you know? And I

personally felt like this was for me a

game-changer being able to describe

the methods the way I describe the data

too, you know? And yeah, I think there's

an audience.

I'm surprised that not a lot of people

talk about this publicly. That was

something when I was writing the talk.

Um, and I'm really sorry I don't have a

write-up on this. Maybe I'll do it one

day. Maybe I can share all the code. But

when the game is out like I said, you

can compile and see how it's done. So,

yeah.

Uh, very simple too.

>> Well, thank you. Give him a

hands.

>> Thanks.


</details>