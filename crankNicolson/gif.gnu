set terminal gif animate delay 5
set output 'foobar.gif'
stats 'data.data' nooutput
set xrange [0:5000]
set yrange [0:.01]

do for [i=1:int(STATS_blocks)] {
    plot 'data.data' index (i-1)
}
