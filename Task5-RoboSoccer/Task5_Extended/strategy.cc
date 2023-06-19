
#include "naobehavior.h"
#include "../rvdraw/rvdraw.h"

extern int agentBodyType;

void NaoBehavior::beam( double& beamX, double& beamY, double& beamAngle ) {
    beamX = -HALF_FIELD_X + worldModel->getUNum();
    beamY = 0;
    beamAngle = 0;
}


SkillType NaoBehavior::selectSkill() {

    VecPosition target;
    
    double opp_y;
    //opp_y = worldModel->getOpponent(&i).getY();
    opp_y = (worldModel->getWorldObject(WO_OPPONENT1)->pos).getY();
    
    target.setX(ball.getX() - 2);
    target.setY(opp_y);
    target.setZ(0);

    return goToTarget(target);    

}
