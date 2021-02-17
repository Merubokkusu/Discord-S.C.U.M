# Reading Discum
Structure of Discum: https://docs.google.com/drawings/d/1_PSefOb5nlqEyEAQ14zPfFQuu8hUh9HVJHuV-ymSnTo/edit?usp=sharing

## need your help:
_(btw each horizontal line in the diagrams below represents a thread, run right after a response from discord's gateway)_          
Alright so currently, for the gateway, the response loop reads a copy of the command list, which means that any modifications to the command loop during the response loop will not show for response loops started before the current point in time. In the diagram below, you can see some of the pros and cons:          
![current method](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/tempReadingImages/first.png)           

Previously, discum had implemented a method which live-updated deletions (after the current point in time):            
![previous method](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/tempReadingImages/previous.png)           
This was removed because of the inconsistency: if deletions are live-updated, then shouldn't also additions be live-updated?            
            
So...this brings us to a method that hasn't been implemented yet into discum (I have the code for it, but it's kinda messy rn). The following live-updates additions and deletions (after the current point in time):            
![idea](https://github.com/Merubokkusu/Discord-S.C.U.M/blob/master/docs/tempReadingImages/idea.png)            
Essentially what it does is uses a linked list, which gives it that kind of flexibility. But, idk, what do you all think? Which method would be the most useful and the least annoying?             
Anyway, feel free to make an issue to let us know (and why you think so). Thanks! :)            
