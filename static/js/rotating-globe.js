var diameter = 150,
    radius = diameter >> 1,
    velocity = .01,
    then = Date.now();

var projection = d3.geo.orthographic()
    .scale(radius - 2)
    .translate([radius, radius])
    .clipAngle(90)
    .precision(0);

var path = d3.geo.path()
    .projection(projection)
    .pointRadius(15);

function rotate_sphere(yaw, pitch, roll) {

    d3.json("/static/data/custom.json", function(error, world) {
        if (error) throw error;

        var r01 = topojson.feature(world, world.objects.pointa);
        var r02 = topojson.feature(world, world.objects.pointb);
        var r03 = topojson.feature(world, world.objects.pointc);
        var r04 = topojson.feature(world, world.objects.pointd);
        var r05 = topojson.feature(world, world.objects.pointe);
        var r06 = topojson.feature(world, world.objects.pointf);
        var r0s = [r01,r02,r03,r04,r05,r06]

        var r1 = topojson.feature(world, world.objects.trianglea);
        var r2 = topojson.feature(world, world.objects.rhombus);
        var r3 = topojson.feature(world, world.objects.diamond);
        var r4 = topojson.feature(world, world.objects.triangleb);

        var globe = {
            type: "Sphere"
        };

        var rotate_path = [yaw, pitch, roll];
        var imu_canvas = document.getElementById("imu_canvas");
        var context = imu_canvas.getContext("2d");
        projection.rotate(rotate_path);
        context.clearRect(0, 0, diameter, diameter);
        context.fillStyle = "#1ab188";
        context.strokeStyle = "#1ab188";


        // for (var i=0; i<r0s.length; i++)
        // {
        //   context.beginPath(), path.context(context)(r0s[i]), context.fill();
        // }

        context.fillStyle = "#1ab188";
        context.beginPath(), path.context(context)(r4), context.fill();
        // context.fillStyle = "#1ab188";
        // context.beginPath(), path.context(context)(r1), context.fill();
        context.fillStyle = "#dddddd";
        context.beginPath(), path.context(context)(r3), context.fill();

        context.beginPath(), path(globe), context.stroke();

        context.strokeStyle = "#000000";

        context.beginPath();
        context.moveTo(0, diameter/2);
        context.lineTo(diameter, diameter/2);
        context.stroke();

        context.beginPath();
        context.moveTo(diameter/2, 0);
        context.lineTo(diameter/2, diameter);
        context.stroke();


    });
}
