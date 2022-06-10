**TASK**
1. Defender’s y-coordinate should change as per balls position.
2. 2 Players strategy:   where bot passes (kicks) ball towards one other. While passing, the other should move straight towards goal.

---
# Part-2
STRATEGY:

> Find the player closest to ball. (say it's player2)

// PLAYER-2

> Ask it to go towards the ball
> 
> Kick towards teammate
> 
> Kick towards goal if closer to goal

// PLAYER-1

> Ask it to move straight along x-axis.
> 
> Stop when closer to goal
> 
> Stop when teammate about to kick







# for Part-1

SkillType NaoBehavior::selectSkill() {

    VecPosition target = VecPosition(me.getX(), ball.getY(), 0);

        return goToTarget(target);    

}

# Update
// Defender's y-coordinate = Opponent's y  &&  Defender's x-coordinate = Ball's x - 2

SkillType NaoBehavior::selectSkill() {

    VecPosition target;

    double opp_y;
    opp_y = (worldModel->getWorldObject(WO_OPPONENT1)->pos).getY();
    
    target.setX(ball.getX() - 2);
    target.setY(opp_y);
    target.setZ(0);

    return goToTarget(target);    

}

