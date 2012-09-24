## Why do you need it

Neji (www.pythonschool.info) is a cooperative coding environment allowing you to code together with your friend or
with a coach. When you strating learning how to code it's easy to get confused and get demotivated by annoying yet simple
errors. This is when coaching could help you get through the first level of weeds and build enough confidence to code
independently.

## History of the project

I coded Neji as my weekend project on Sept 15th and 16th 2012.

The service is coded in Python and running on Django platform (for web pages) and [Tornado](http://www.tornadoweb.org)
(for WebSockets).
At the client side I use Twitter Bootstrap framework and [Ace code editor](http://ace.ajax.org).
I used [Bount](https://github.com/mturilin/bount) cloud deployment system to create execution environment for the
production server.

## Limitations

Neji doesn't support python "import" statement for arbitrary packages because it would effectively give a guest access
to the server to anybody. The list of the allowed packages is on the Python page.

Also, I need to protect the server from inifinite tasks. For example, somebody could write an inifinit loop and load
the server indefinitely. To prevent this, the running time of the each task is limited to 5 seconds. Please, let me know
if you think this limited should be lifted.

## Future plans

I have quite a few future plans about it.

Some of the ideas how improve Neji as standalone project:

- Add cloud login system using [Akamaru](https://github.com/mturilin/akamaru) (drop-in social authentication system for Django)
- Make Neji a Facebook application enabling cooperative coding right on the Facebook web site
- Create a collaborative coding environment for the more serious projects

Also, Neji could be integrated to a bigger learning platform:

- Integrate with some free learning service, like Khan academy
- Integrate with open source learning management system like, [Moodle](http://moodle.org) or [Class2Go](http://class2go.stanford.edu)
- Integrate into a commercial learning system, like my own [GetCCNA](http://getccna.ru) (the web site is in Russian)


## About Neji character

This project is name after [Neji Hyuga](http://naruto.wikia.com/wiki/Neji_Hyūga), an anime character from [Naruto
universe](http://naruto.wikia.com/wiki/Narutopedia).

![Neji's picture](http://f.cl.ly/items/0M1T011E1X2V2m37463D/1000px-Neji's_Byakugan.PNG)

## About me

My name is Mikhail Turilin, I'm a developer and product manager living in San Francisco, CA. My
professional resume is available here:
[View PDF](http://f.cl.ly/items/421n3o2q1i3g0x3c132v/Mikhail%20Turilin%20-%20Product%20Manager%20Resume%202012.pdf)

My GitHub home is here: [github/mturilin](http://github/mturilin)

You can contact me by [mturilin@gmail.com](mailto:mturilin@gmail.com) or Twitter [@mturilin](http://twitter.com/mturilin).

## Code and Licensing

Neji code is available on GitHub: [https://github.com/mturilin/neji](https://github.com/mturilin/neji)

Neji is GPL v3 licensed: [http://www.gnu.org/copyleft/gpl.html](http://www.gnu.org/copyleft/gpl.html)