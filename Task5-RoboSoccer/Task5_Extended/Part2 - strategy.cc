#include "naobehavior.h"
#include "../rvdraw/rvdraw.h"

extern int agentBodyType;

void NaoBehavior::beam( double& beamX, double& beamY, double& beamAngle ) {
    beamX = -HALF_FIELD_X + 5;
    if(worldModel->getUNum() == 1)
        beamY = 5;
    else
        beamY = -5;
    beamAngle = 0;
}


SkillType NaoBehavior::selectSkill() {

    int playerNum = getPlayerClosestToBall();

    int teammate;
    if(playerNum == 1)
        teammate = 2;
    else
        teammate = 1;

    if(worldModel->getUNum() == playerNum) {

        // Walk to ball
        if (me.getDistanceTo(ball) > 1) {
            return goToTarget(ball);
        } 
        //kick towards goal if closer to goal
        else if(me.getX() >= HALF_FIELD_X-3)
            return kickBall(KICK_FORWARD, VecPosition(HALF_FIELD_X, 0, 0));
        
        // Kick ball towards teammate
        else {
            VecPosition target = worldModel->getWorldObject(teammate)->pos;
            return kickBall(KICK_FORWARD, target);
        }       
    }

    else {
        //stand if closer to goal
        if(me.getX() >= HALF_FIELD_X-3) {
            return SKILL_STAND;
        }

        //wait when teammate about to kick
        VecPosition teammate_pos = worldModel->getWorldObject(playerNum)->pos;
        if(teammate_pos.getDistanceTo(ball) < 0.5) {
            return SKILL_STAND;
        }
        
        //move straight along x-axis
        return goToTarget(VecPosition(me.getX() + 3,me.getY(),0));
    }   
}

int NaoBehavior::getPlayerClosestToBall() {
    
    VecPosition pos;
    double dist1, dist2;
    if(worldModel->getUNum() == 1) {
        dist1 = me.getDistanceTo(ball);
        
        //teammate
        pos = worldModel->getWorldObject(WO_TEAMMATE2)->pos;
        dist2 = pos.getDistanceTo(ball);

        if(dist1 < dist2) {
            return(1);
        }
        else {
            return(2);
        }
    }

    //else if(worldModel->getUNum() == 2) {
    else {
        dist2 = me.getDistanceTo(ball);
        
        //teammate
        pos = worldModel->getWorldObject(WO_TEAMMATE1)->pos;
        dist1 = pos.getDistanceTo(ball);

        if(dist1 < dist2) {
            return(1);
        }
        else {
            return(2);
        }
    }
}
