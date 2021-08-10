classdef ObjectClass < handle
    properties
        % status
        color
        alpha
        sound
        % devices
        display
        width
        height
        receiver
        speaker
        emitter
    end
    methods
        function obj = ObjectClass()
            obj.display = wb_robot_get_device('display');
            obj.width = wb_display_get_width(obj.display);
            obj.height = wb_display_get_height(obj.display);
            obj.receiver = wb_robot_get_device('receiver');
            wb_receiver_enable(obj.receiver, 32);
            wb_receiver_set_channel(obj.receiver, 1);
            obj.speaker = wb_robot_get_device('speaker');
            obj.emitter = wb_robot_get_device('emitter');
            wb_emitter_set_channel(obj.emitter, 2);
        end
        step(obj)
        set_color(obj, color, alpha)
    end
end