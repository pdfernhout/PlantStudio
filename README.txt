The PlantStudio program as released around 1997 was originally developed under Delphi Pascal for Windows. Much earlier versions were also for a time before that developed in VisualBasic, C++, and Smalltalk as well but would be of little general interest compared to this code.

The PlantStudio software was developed by Cynthia Kurtz and Paul Fernhout working together as "Kurtz-Fernhout Software", who jointly hold the copyright to that code.

The system uses an infrastructure developed for the GPL'd "Garden with Insight" Garden Simulator the two wrote together earlier.

Cynthia was the primary developer of the PlantStudio code. Paul developed most of the infrastructure and the 3D turtle code it uses. 

The 3D library it uses as of this release is a custom 3D turtle. It would make a lot of sense at this point to port that part to use OpenGL or something similar.

The current released code includes the Delphi source, but not in an an easily buildable state. Attempts to get that source to run under the Lazarus/FPC Delphi-work-alike system encountered some usual issues,  but in theory getting it runnable under Lazarus would be possible with some rewriting of Win32 specific code.

A translator was created by Paul to convert the Delphi code to Python and Java (as a rough imperfect conversion requiring later clean-up by hand). That translator converted, say, uabout.pas into uabout.pas.py and uabout.pas.java (as well as creating an intermediate uabout.pas.pickle file  that can be ignored or discarded). The results of that translation is in the "converted source" directory. But such code needs further work to get it running right. As each file was used, it was moved to the "used" subdirectory there.

Work was done by Paul to get that code working under Jython (Swing) and for the OLPC (GTK). Those attempts are in the "for-jython" and "for-olpc-python" respectively. A lot of those files in those two directories are duplicates of each other and that should be cleaned up. The focus there was on getting the core drawing code and data reading code working.

That work is not complete, however. The interactive GUI code itself was mostly not used. Part of the reason is that the GUI should really be redone. The older GUI focused on things like creating bouquets of plants, but PlantStudio would probably be better as a tool more focused on breeding plants and maintaining a library of plants. Composition of plants done in other tools (like Blender or whatever) designed for that task.

The OLPC version does run and draw plants, although slowly. Profiling information is included there. Basically the slowest point there is just on an inner loop lookup of colors and should be fairly easy to improve. That bottleneck would all get replaced with a move to OpenGL though.

So, there are at least four options for anyone wanting to work with the code.
* Get the Delphi code as is to work with something like Lazarus.
* Expand on the Python version of the core code, writing a new GUI.
* Expand on the Java version of the core code, writing a new GUI.
* Port the code to some other language you like better.

Right now, improving on the Python code is probably the easiest way to go.

We would also love to see it as, say, a Blender plugin.

Ideally, someday, we wanted to generalized this code to work with arbitrary sets of parameters to be able to breed any kind of 3D model. Maybe someday someone will do that. We enjoyed working on the PlantStudio software, and we hope you have fun playing around with it too. We picked the GPL v3 or  later license, as a sort of constitution for collaboration on the code.

You can find some similar "breeding" ideas in an Android App that Paul wrote called "EvoJazz"  for breeding new musical phrases.
  https://market.android.com/details?id=com.evojazz
  
So, these ideas can be used in lots of ways to create more abundance of interesting patterns in the world.

=== On motivations

Related on motivation by Dan Pink:
  "RSA Animate - Drive: The surprising truth about what motivates us"
  http://www.youtube.com/watch?v=u6XAPnuFjJc
  
And: "If you love somebody, set them free (Sting)"

And someday we may see a balance shift between five interwoven economies in a way that gives more people more time for making more free stuff (whether through a basic income, 3D printing, more gift giving, or better democratic planning), as Paul talks about in this video:
  "Five Interwoven Economies: Subsistence, Gift, Exchange, Planned, and Theft"
  http://www.youtube.com/watch?v=4vK-M_e0JoY

We hope everyone out there is getting the right amount of vitamin D, since humans need sunlight, just like plants. We both became vitamin D deficient working indoors so much on computers, and it was bad for our health. We should have tried to think more like plants. :-)

Plants can also make you well in more ways than psychologically by looking at them and caring for them. If you eat a lot of vegetables, fruits, and beans, listening to people like Dr. Joel Fuhrman, while nothing is certain in life, you can probably avoid or delay a lot of health issues  like heart disease, cancer, diabetes, dementia, and so on. Paul lost fifty pounds to return to a healthy weight and lower his blood pressure significantly by following that kind of advice. It's helping Cynthia too. The battle of the bulge is mostly fought and won in the supermarket. We wish we had appreciated the miracle of healing through plants a lot earlier in life.

One of the most funny/ironic things anyone ever sent us was a link to a "How To" they wrote  with the title "Quake goes Floral" about using PlantStudio to add some vegetation to Quake. Somehow, that seemed really hopeful.

We hope whatever world you live in, it has a lot of interesting and beautiful plants in it (both real and virtual). Ideally we hope those plants could grow in world  that is happy, healthy, joyful, abundant, and intrinsically/mutually secure for all. It has been an honor, and a privilege to help create tools to help others create such worlds (and, even with a lot of ups and downs along the way, a lot of "hard fun" as well).

--Paul Fernhout and Cynthia Kurtz
July 6, 2011
