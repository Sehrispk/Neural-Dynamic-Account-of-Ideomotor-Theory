% MATLAB controller for Webots
% File:          ObjectController.m
% Date:          10.08.21
% Description:   ObjectController for Simulation environment
% Author: Stephan Sehring

TIME_STEP = 64;

% get Object Class
Object = ObjectClass();

% set box color, transparency and cue status
Object.set_color([1 0 1], 1.);
Object.sound = 'TestSound.wav';
cue = 1;

while wb_robot_step(TIME_STEP) ~= -1
  if cue 
  cue = 0;
  wb_speaker_play_sound(Object.speaker, Object.speaker, Object.sound, 1, 1, 0, 0);
  tic
  end
  Object.step();
end
