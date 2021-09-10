function obj = step(obj)
  % status
  que = wb_receiver_get_queue_length(obj.receiver);
  listen = (que > 0);
  if listen
    distance = 1. / sqrt(wb_receiver_get_signal_strength(obj.receiver));
  end
  play = wb_speaker_is_sound_playing(obj.speaker, obj.sound);
  
  % act
  if listen && play == 0 && distance < 0.2
    if toc > 10
      wb_speaker_play_sound(obj.speaker, obj.speaker, obj.sound, 1, 1, 0, 0);
    end
    tic
  end
  if play
    wb_emitter_send(obj.emitter, 2);
  end
  if listen
    wb_receiver_next_packet(obj.receiver);
  end
  
  end