#include "naobehavior.h"
#include "../rvdraw/rvdraw.h"

extern int agentBodyType;

/*
 * Real game beaming.
 * Filling params x y angle
 */
void NaoBehavior::beam( double& beamX, double& beamY, double& beamAngle ) {
    beamX = -HALF_FIELD_X + worldModel->getUNum();
    beamY = 0;
    beamAngle = 0;
}


SkillType NaoBehavior::selectSkill() {

    return newStrategy();    
}

SkillType NaoBehavior::newStrategy(){

    if (me.getDistanceTo(ball) > 1) {
            // Walk to ball
            return goToTarget(ball);
    } 
    else {
            // Kick ball towards opponent's goal
            return kickBall(KICK_DRIBBLE, VecPosition(HALF_FIELD_X, 0, 0));
        }
}


