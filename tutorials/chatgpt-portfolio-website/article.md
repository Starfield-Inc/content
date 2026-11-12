---
title: "ChatGPT tutorial: How to create a website with ChatGPT"
seo_title: "Build a Website with ChatGPT: AI Hackathon Tutorial"
meta_description: "AI hackathon tutorial: build a responsive Bootstrap portfolio site with ChatGPT prompts, from the HTML skeleton to the contact form."
---

[ChatGPT](https://openai.com/blog/chatgpt/) drew a lot of attention when it launched: people shared their conversations with it and its answers to many problems. They also shared insights about its ability to write code, but we are not going to talk about that in general terms. In this tutorial we will create a website using ChatGPT.

## Building a website in an AI hackathon

A landing page or portfolio site is often the first thing an AI hackathon team needs for a demo. Using ChatGPT for the first draft saves time, as long as you check what it gives you. When you want to build an app on ChatGPT and other new technologies, see the [upcoming AI hackathons](/ai-hackathons/).

## Make a website with ChatGPT

First, I entered my prompt:

*Create an html skeleton with bootstrap responsive design and responsive menu and responsive hamburger menu that works on mobile as well. And import all the necessary scripts before the closing body tag, such as jquery, popper and bootstrap.*

It looks like we got a correct response from ChatGPT, but to be sure let's check it in [replit](https://replit.com/) and continue working with it there.

We can see that the page is working but the mobile menu isn't. It also seems that ChatGPT chopped the skeleton a bit and we don't have a closing tag for one script, and if we check https://getbootstrap.com/docs/4.1/getting-started/introduction/ we can see that the bootstrap script is missing. So let's fix it. I will also change the imports to the latest ones based on the bootstrap introduction.

```html
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>My Website</title>
<!-- Bootstrap CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css"
integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous" />
</head>

<body>
<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
<a class="navbar-brand" href="#">My Website</a>
<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="navbarNav">
<ul class="navbar-nav">
<li class="nav-item active">
<a class="nav-link" href="#">Home</a>
</li>
<li class="nav-item">
<a class="nav-link" href="#">About</a>
</li>
<li class="nav-item">
<a class="nav-link" href="#">Contact</a>
</li>
</ul>
</div>
</nav>

<!-- Page content -->
<div class="container mt-5">
<h1>Welcome to My Website!</h1>
<p>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ornare
magna eros, eu pellentesque tortor vestibulum ut. Maecenas non massa
sem. Etiam finibus odio quis feugiat facilisis.
</p>
</div>

<!-- Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js"
integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49"
crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js"
integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy"
crossorigin="anonymous"></script>
</body>

</html>
```

Now it's working. Let's work on the content. I would like to have a portfolio site.

## What should be the title?
First of all, what should be the title? I asked ChatGPT, as it's doing the job:

**What should be my portfolio website title?**

I will go with "Jane Doe - Beginner AI user".

## Introduction for the website

*Write an introduction for my portfolio website. I am a beginner AI user and a programmer.*

Paste the introduction ChatGPT gives you into the page.

## Create an image element on that page

*Show me an image element with a mountain for the bootstrap page.*

I will use a mountain image from lorempicsum

```html
<img src="https://picsum.photos/id/29/600/600" class="img-fluid rounded" alt="Mountain">
```

This will be a single page for the sake of simplicity.
Let's add an id for the home part and let's add href to the anchor tags corresponding to the sections.

```html
<li class="nav-item active">
<a class="nav-link" href="#home">Home</a>
</li>
<li class="nav-item">
<a class="nav-link" href="#about">About</a>
</li>
<li class="nav-item">
<a class="nav-link" href="#contact">Contact</a>
</li>
```

## Making the about section

*Create a text about me for an about page on a website. I like rock climbing and all outdoor sports and I like to program. I started my career as a Quality engineer in the automotive industry but I was always curious about programming. I started with automation and microcontroller programming. I started web development by myself 4 years ago with HTML and JavaScript. I am working now as a Full Stack Developer.*

Paste the text ChatGPT returns into the about section.

We need to make this section as high as the device. Therefore I asked ChatGPT to show me the correct way to do it.

*How to make an element high as the device in bootstrap?*

I will follow the instructions: paste the styling in the head tag and add the class to the div element that contains the section.

## Creating the contact section as a form. (We won't make this working in this tutorial)

*Create a contact form with Bootstrap with the following input fields. Name, email, message.*

```html
<form>
<div class="form-group">
<label for="name">Name</label>
<input type="text" class="form-control" id="name" placeholder="Enter your name">
</div>
<div class="form-group">
<label for="email">Email</label>
<input type="email" class="form-control" id="email" placeholder="Enter your email">
</div>
<div class="form-group">
<label for="message">Message</label>
<textarea class="form-control" id="message" rows="3" placeholder="Enter your message"></textarea>
</div>
<button type="submit" class="btn btn-primary">Submit</button>
</form>
```

So let's copy this and create the section for the Contact form.

And finally, let's create a nice background for the website.

*What is a nice css gradient for an html website background that is not too bright?*

I pasted the result in a style tag in the head tag.

```css
body {
background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
}
```

And it is ready. Not perfect, but working. I am not suggesting creating your whole portfolio website with ChatGPT, but it can give some good tips and can improve your work, or at least make it easier and less time consuming.

## Frequently asked questions

**How do I get a first HTML skeleton from ChatGPT?**

Ask it for an HTML skeleton with Bootstrap responsive design, a responsive hamburger menu, and the jQuery, Popper and Bootstrap scripts before the closing body tag. Then check the result in an editor such as Replit.

**Is the ChatGPT output ready to use as it is?**

Not always. In this tutorial the mobile menu did not work at first, one script was missing a closing tag and the Bootstrap script was missing, so the imports had to be fixed by hand.

**Does the contact form work?**

No. The tutorial only creates the form fields (name, email, message) and a submit button and does not make the form send anything.

## How this tutorial was tested

This content was carried over from an earlier tutorial and updated for Starfield Labs. It was not re-run in this build, and no step in it has been tested here. To follow it you need a ChatGPT account (a paid plan may be needed for some models) and a free Replit or other editor account. None of these was used for this write-up.
