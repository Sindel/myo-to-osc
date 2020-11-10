		n = NetAddr.new( "127.0.0.1" , 2000 ); // for sending messages to MiniBees

		thisProcess.openUDPPort(7110); // open port 57120 - for miniBees

		n.sendMsg( "/run", 4, 0, 0, 1); //Turn on the Status LED on the ground MiniBee.
		n.sendMsg( "/kill", 4, 0, 0, 1); //Turn on the Status LED on the ground MiniBee.

first myo
n.sendMsg( "/myo/activate", "f7:9a:4a:68:04:8c", 1); //to run
n.sendMsg( "/myo/activate", "f7:9a:4a:68:04:8c", 0); //to kill

second myo
n.sendMsg( "/myo/activate", "d9:16:12:8b:cd:aa", 1); //to run
n.sendMsg( "/myo/activate", "d9:16:12:8b:cd:aa", 0); //to kill


on raspberry:
		n = NetAddr.new( "192.168.1.103" , 2000 ); // for sending messages to MiniBees
		thisProcess.openUDPPort(3000);
OSCdef.trace(false)
OSCdef.trace()
on raspberry via other modem:
		n = NetAddr.new( "192.168.1.2" , 2000 ); // for sending messages to MiniBees
		thisProcess.openUDPPort(3000);
OSCdef.trace(false)
OSCdef.trace()
		n = NetAddr.new( "192.168.1.4" , 2000 ); // for sending messages to MiniBees


		n = NetAddr.new( "127.0.0.1" , 2000 ); // for sending messages to MiniBees


