Why you should pick open-source tools as a developer
2026/05/01
linux,setup,workstation

## Programming, a craft
I've used several closed-source, proprietary tools for a long time as a
developer, but all of them left a bad taste in my mouth.

First, I have to talk good things about proprietary software I've used.

I've never encountered a problem on Windows that wouldn't be solved by a clean
reinstall of the software, sure that meant messing around with _Regedit_ and
maybe hidden folders on _C:\\Windows_, but it was never a HUGE problem, like
the ones you find when debugging Pulseaudio on Linux, for example.

I've never had bad UI/UX experiences with VSCode\*. Or with the
JetBrains Debugger. The good part about proprietary software is that its
usability is generally more smooth for the base-case than open source.

Open-source, in my experience, can
generally have 'idiotic' things. Such as Linux's major GUI not having thumbnails
for the file picker browser for over 20-something years.

For long, I thought that the use of proprietary tools as a programmer made more 
sense since they were made by professionals, and open source for me was the
eternal archetype of **Richard Stallman playing Super Tux Kart**.

I also would think that the same way that miners don't (necessarily) have the 
know-how to make a pickaxe, the programmer shouldn't really care about how and
his tools are made, or care about the tools at all. 

In the next sections, I'll draft a general idea on why you should consider
caring about your tools.

## The mindset shift
First thing is, a pickaxe isn't vendor locked. Also, the manufacturer can't
really FORCE YOU NOT TO use a pickaxe by just removing some files on a server.

### Visual Studio For Mac
Visual Studio for Mac suffered this fate. I've never used it, but its a
clear case of how companies can just press Shift+Del on a piece of locked-in
software. Nowadays, you can download the, already pretty disgusting,
web-installer, but all the files that were downloaded by the installer were
deleted by Microsoft. 

All the people who relied on Microsoft's software were now forced to migrate to
closed-source Rider (for C#) or other alternatives such as VSCode.

### Windows 11
Windows 11 broke the 'Metro UI' that was used by Microsoft since Windows 8,
which for some was a scandal. What if Microsoft just arbitrarily changed the
"disable mouse acceleration" button? What if they forced an AI tool into it?

I've never seen this huge philosophy difference between open and closed-source
software, for me it was just a matter of public development, licenses and so on.

This is what made my mind shift: the free and open-source can live forever.

## Built to last
Linus Torvalds uses the same version of uEmacs that he used in the 1990s.
As long as you have the source code and the ability to tweak some of the build
process or dependencies, you can use the software basically forever.

Not the company, nor the guy who wrote it, neither the ones who host the
source-code will lock you out of it. If I want to use, for some reason,
my neovim 0.10.0 on a very old Linux, or 20 years in the future, why couldn't I?
I have the source code, and programming skills, that's enough. 

That's the beauty of open source, people are still building Firefox for Windows 7
even though Mozilla has stopped the development, some people still patch Rust,
Firefox, Chromium to work on out-of-date operating systems.

The idea of using the same GUI **forever** is pretty common on Linux.

If for some reason you liked `wmii`, you can just download the source code, and
possibly make some fixes for it to compile and voilá. Or even better, someone
could've already done it, and you can just download the fork, or the PKGBUILD,
whatever.

## Key takeaways

Tmux will last forever.
Neovim will not get a random AI chat thingy when I next open it.
i3 will always create a new window on Super+Return.

Also, if you want a more utilitarian argument:

using the same portable open-source tools builds consistency,
muscle memory and it's boring enough so you can focus on your work.


I should be able to install my tools on possibly every operating system with UNIX utilities
and a C compiler.


---
_1. VSCode as in the software released by Microsoft is proprietary. You cannot
reproduce the builds you download._
