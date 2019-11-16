Use raw map to compute what the car is hitting

Check that the car image is put on the center posx posy

The segments are a convenient place to init the car pos and direction randomly

The map might create all the segments reversed (add 180 to direction, center stays there)

Change logg.critical to exception raised

Remove sacollisions and reward as arguments of render, they always exist

