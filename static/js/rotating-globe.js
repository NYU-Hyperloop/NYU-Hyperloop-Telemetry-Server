
        var diameter = 180,
            radius = diameter >> 1,
            velocity = .01,
            then = Date.now();

        var projection = d3.geo.orthographic()
            .scale(radius - 2)
            .translate([radius, radius])
            .clipAngle(90)
            .precision(0);

        var path = d3.geo.path()
            .projection(projection);

        function rotate_sphere(yaw, pitch, roll) {

            d3.json("/static/data/world-110m.json", function(error, world) {
                if (error) throw error;

                var land = topojson.feature(world, world.objects.land);
                var globe = {
                    type: "Sphere"
                };

                var rotate_path = [yaw, pitch, roll];
                var imu_canvas = document.getElementById("imu_canvas");
                var context = imu_canvas.getContext("2d");
                projection.rotate(rotate_path);
                context.clearRect(0, 0, diameter, diameter);
                context.fillStyle = "#1ab188";
                context.strokeStyle = "#ffffff";
                context.beginPath(), path.context(context)(land), context.fill();
                context.beginPath(), path(globe), context.stroke();

            });
        }