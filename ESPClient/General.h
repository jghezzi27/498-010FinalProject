#pragma once

enum SystemState {
  ACTIVE,
  APPROVED,
  REJECTED,
  RESTING,
  ERRORSTATE
};

enum LockState {
  LOCKED,
  UNLOCKED
};

void DoActive();
void DoApproved();

void ToActive();
void ToApproved();
