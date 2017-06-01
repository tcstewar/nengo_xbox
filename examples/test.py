import nengo
import nengo_xbox

model = nengo.Network()
with model:
    xbox = nengo_xbox.Xbox()

    nengo.Connection(xbox.axis[4:], xbox.vibrate)