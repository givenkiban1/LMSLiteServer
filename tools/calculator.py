from wolframclient.evaluation import WolframLanguageSession

from wolframclient.language import wl, wlexpr

session = WolframLanguageSession()

e = session.evaluate(wl.WolframAlpha("number of moons of Saturn", "Result"))

print(e)



# https://github.com/aunyks/newton-api