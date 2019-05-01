# sabermetrics-2k19-project

+ Author: Brandon Aguirre
+ Section: CSCI 4831
+ Professor: Rhonda Hoenigman

---

## Description

# AWPS - Aguirre's Wager Point System

## Description & Inspiration

Below I implement a closed point rating system. I’ll define a “closed point” rating system to be a rating system that distributes a finite number of points to all players in the MLB. These points will be transferred between pitchers and batters each time a pitcher and batter face off.

I was inspired to create this rating system by the Hungarian-American physicist Arpad Elo who invented the Elo Rating System. His system was used to rate chess players based on their relative skill levels. I expect that the Elo Rating System was a bit simpler to implement because the points were transferred between two players who played the same position (both are chess players). The point system I am implementing will be transferring points between two players who play different positions - pitcher and batter, and will have to take into account different events.


## AWPS can replace some metrics

AWPS takes into account singles, doubles, triples, homeruns, and strikeouts. For Batters this means it could replace batting avg, and slugging percentage. AWPS weights homeruns higher than singles, doubles, and triples. The issue with this is that it does not take into account at bats. So AWPS doesn't give a very accurate picture of a players entire career.

What AWPS is good at, is giving an decent representation of a players performance over a season. What AWPS is great at is giving an accurate representation of a players recent performance. AWPS changes quickly as a result of wins losses to between a pitcher and batter. The more you lose points, the faster you lose points. This is because AWPS weights the number of points a player gains depending on the number of points they already have.

Another benefit to AWPS over batting avg, or slugging percentage, is that it weights the number of points between each face off, by the skill level of the players involved. That means if a great batter gets a lot of hits from a crappy pitcher, their AWPS score won't inflate. However, if a batter is on a bad streak due to an injury or some unseen problem, they will lose points quickly if they are getting "beat by a bad pitcher".

[wiki elo rating system]: https://en.wikipedia.org/wiki/Elo_rating_system

### Check out the math here!

[Aguirre's Wager Point System Jupyter Notebook](https://github.com/brancisco/sabermetrics-2k19-project/blob/master/src/aguirres-wager-point-system.ipynb)

### Check out the web app here!

[Aguirre's Wager Point System App](https://brancisco.github.io/sabermetrics-2k19-project/)
