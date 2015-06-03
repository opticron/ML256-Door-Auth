import sys
import pjsua as pj

# Logging callback
def log_cb(level, str, len):
    print str,

class MyAccountCallback(pj.AccountCallback):
    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)
        
    def on_incoming_call(self, call):
        call.hangup(501, "Sorry, not ready to accept calls yet")
        
    def on_reg_state(self):
        print "Registration complete, status=", self.account.info().reg_status, \
              "(" + self.account.info().reg_reason + ")"
        
# Callback for MyBuddy
class MyBuddyCallback(pj.BuddyCallback):
    def __init__(self, buddy=None):
        pj.BuddyCallback.__init__(self, buddy)

    def on_state(self):
        print "Buddy", self.buddy.info().uri, "is",
        print self.buddy.info().online_text

# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        print "Call is ", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        
    # Notification when call's media state has changed.
    def on_media_state(self):
        global lib
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            lib.conf_connect(call_slot, 0)
            lib.conf_connect(0, call_slot)
            print "Hello world, I can talk!"

def NotifyAsterisk(username):
  print "Username to Announce: " + username

  # Create library instance
  lib = pj.Lib()

  # Init library with default config
  lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))

  # Create UDP transport which listens to any available port
  transport = lib.create_transport(pj.TransportType.UDP)

  # Create Username for authentication
  #acc_cfg = pj.AccountConfig()
  #acc_cfg.id = "sip:" + username + "@doorPi.org"
  #acc_cfg.reg_uri = "sip:doorPi.org"
  #acc_cfg.auth_cred = [ AuthCred("*", "doorPi", "secretpass") ]
  acc_cfg = pj.AccountConfig("doorPi.org", "USERNAME", "PASSWORD")

  acc_cb = MyAccountCallback()

  # Start the library
  lib.start()

  #This line is used because RaspberryPi has no sound input.  Instead we "sudo modprobe snd-dummy"
  snd_dev = lib.get_snd_dev()
  print snd_dev
  #lib.set_snd_dev(0,-1)
  #lib.set_null_snd_dev()

  # Create local/user-less account
  acc = lib.create_account_for_transport(transport)
  #acc = lib.create_account(acc_cfg, cb=acc_cb)
  #acc = lib.create_account(acc_cfg)

  #Create Extra Headers
  header_list = []
  header_list.append(("ML256Username",username))

  sipToCall = "sip:ADDRESS:5060"

  #Create Buddy Instance
  buddy_cb = MyBuddyCallback()
  #myBuddy = pj.Buddy(lib, -1, acc, cb=buddy_cb)
  thisBuddy = acc.add_buddy(sipToCall, cb=buddy_cb)  

  # Make call
  try:
      #Send message
      pj.Buddy.send_pager(thisBuddy, "bagsOfDicks", im_id=0, content_type='text/plain', hdr_list=header_list)

      #call = acc.make_call("sip:ADDRESS:5060", MyCallCallback(), hdr_list=header_list)
  except pj.Error, e:
      print "Exception: " + str(e)
      return None

  # Wait for ENTER before quitting
  print "Press <ENTER> to quit"
  input = sys.stdin.readline().rstrip("\r\n")

  # We're done, shutdown the library
  lib.destroy()
  lib = None
  return

# Check command line argument
#if len(sys.argv) != 2:
#    print "Usage: simplecall.py <dst-URI>"
#    sys.exit(1)

#try:
    # Create library instance
#    lib = pj.Lib()

    # Init library with default config
 #   lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))

    # Create UDP transport which listens to any available port
  #  transport = lib.create_transport(pj.TransportType.UDP)
    
    # Start the library
   # lib.start()

    # Create local/user-less account
    #acc = lib.create_account_for_transport(transport)

    #lib.set_null_snd_dev()

    # Make call
    #call = acc.make_call(sys.argv[1], MyCallCallback())

    # Wait for ENTER before quitting
    #print "Press <ENTER> to quit"
    #input = sys.stdin.readline().rstrip("\r\n")

    # We're done, shutdown the library
    #lib.destroy()
    #lib = None

#except pj.Error, e:
#    print "Exception: " + str(e)
#    lib.destroy()
#    lib = None
#    sys.exit(1)

