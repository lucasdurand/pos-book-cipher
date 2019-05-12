# pos-book-cipher

Check out a working example here, using some D&D source text for the book (Volo's Guide to Monsters): [http://cipher.anvil.app](http://cipher.anvil.app)

## Overview
- Produce a simple cipher from codex text
- Substitution cipher using part-of-speech to form substitution lists from source text

## Not 1:1

This is a good bit of fun, but due to the nature of the constructed cipher text, the context of words can (and will) change, resulting in a shift of POS. The result is that the plain text is generally not fully recoverable. It does a fairly good job though ;)

### Original

> I have not been in this new world very long, but already I am feeling out of place.
> The blade speaks to me now. It is unnerving. 

### Encoded

> I winnowed sometimes determining beneath the next rest temporarily long, and already I am feeling on so making. 
> Both blade speaks out me more. Who provides unnerving.

### Decoded

> I have not been in this new world very long, but already I am feeling out of catch. 
> the blade speaks at me death-fearing. it is unnerving.
