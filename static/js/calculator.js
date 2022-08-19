function CalculateVideos(){

    totalTime = 0;
    var categories = [];

    $.each(g_playlistitemsVideo, function (i, item) {
        totalTime = totalTime + item.videos_duration;

        if (i==0){
            categories[0] = item.categories_name;
        }

        newCategoryFound = true;

        $.each(categories, function (j, category) {
            if (category == item.categories_name){
                newCategoryFound = false;
            }
        });

        if (newCategoryFound){
            categories.push(item.categories_name);
        }

    });

    $('#selVideos').html("Selected videos " + toFormattedTime(totalTime));

}

function toFormattedTime(timeInSeconds){
    timeStr = Math.floor(totalTime/60).toString() + ':' + (totalTime%60).toString() + 's';
    return(timeStr)
}