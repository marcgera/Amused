
var g_categories;
var g_levels;
var g_backgrounds;
var g_videos;
var g_music;
var g_playlists;
var g_playlistitemsMusic
var g_playlistitemsVideo

var g_categorie = 0;
var g_level = 0;
var g_background = 0;
var g_selectedVideo= 0;
var g_selectedMusic = 0;
var g_playlist = 0;
var g_playlistitemMusic = 0;
var g_playlistitemVideo = 0;
var modal;
var modalEdit;

$(document).ready(function () {

    modal = document.getElementById("myModal");
    modalEdit = document.getElementById("ModalEdit");

    $.get("/getCategories", function (data, status) {
        g_categories = JSON.parse(data);
        $.each(g_categories, function (i, item) {
            $('#categories').append($('<option>', {
                value: item.ID,
                text: item.categories_name
            }));
        });
    });

    $.get("/getLevels", function (data, status) {
        g_levels = JSON.parse(data);
        $.each(g_levels, function (i, item) {
            $('#levels').append($('<option>', {
                value: item.ID,
                text: item.levels_name
            }));
        });
    });

    $.get("/getBackgrounds", function (data, status) {
        g_backgrounds = JSON.parse(data);
        $.each(g_backgrounds, function (i, item) {
            $('#backgrounds').append($('<option>', {
                value: item.ID,
                text: item.backgrounds_name
            }));
        });
    });

    GetPlayLists();

    function GetPlayLists() {
        $('#playlists').empty();
        $.get("/getPlaylists", function (data, status) {
            g_playlists = JSON.parse(data);
            $('#playlists').empty();
            $.each(g_playlists, function (i, item) {
                $('#playlists').append($('<option>', {
                    value: item.ID,
                    text: item.playlists_name
                }));
            });
        });
    }

    $('#categories').on('change', function () {
        g_categorie = g_categories[this.selectedIndex];
        doFilter();
    });

    $('#levels').on('change', function () {
        g_level = g_levels[this.selectedIndex];
        doFilter();
    });

    $('#backgrounds').on('change', function () {
        g_background = g_backgrounds[this.selectedIndex];
        doFilter();
    });

    $('#videos').on('change', function () {
        g_selectedVideo= g_videos[this.selectedIndex];
        doCheck();
    });

    $('#music').on('change', function () {
        g_selectedMusic = g_music[this.selectedIndex];
        doCheck();
    });

    $('#add2playlist').on('click', function () {
        doAdd2Playlist();
    })

    $('#add2playlist').on('click', function () {
        doAdd2Playlist();
    })


    $('#removePlaylist').on('click', function () {
        doRemovePlaylist();
    })

    $('#removeFromplaylist').on('click', function () {
        doRemoveFromPlayList();
    })

    $('#VideoUp').on('click', function () {
        doMovePlayListItem('playlist_videos', 'up');
    })

    $('#VideoDown').on('click', function () {
        doMovePlayListItem('playlist_videos', 'down');
    })

    $('#VideoRemove').on('click', function () {
        doRemovePlayListItem('playlist_videos', g_playlistitemVideo);
    })

    $('#MusicUp').on('click', function () {
        doMovePlayListItem('playlist_music', 'up');
    })

    $('#MusicDown').on('click', function () {
        doMovePlayListItem('playlist_music', 'down');
    })

    $('#MusicRemove').on('click', function () {
        doRemovePlayListItem('playlist_music', g_playlistitemMusic);
    })

    $('#play').on('click', function () {
        window.open("http://127.0.0.1:81/playlist?playlist_ID=7");
    })

    $('#playlists').on('change', function () {
        g_playlist = g_playlists[this.selectedIndex];
        doFillPlayListItemsVideo();
        doFillPlayListItemsMusic();
    });

    $('#addPlaylist').on('click', function () {
        modal.style.display = "block";
        $('#playlist_name').focus();
    })


    $('#editPlaylist').on('click', function () {
        modalEdit.style.display = "block";
        $('#playlist_name_edit').focus();
    })

    $('#addPlaylist2').on('click', function () {
        addPlayList();
    })

    $('#editPlaylistName').on('click', function () {
        editPlayListName();
    })

    $('#selectedVideos').on('change', function () {
        g_playlistitemVideo = g_playlistitemsVideo[this.selectedIndex];
        doPlayListItemsVideosChanged(this.selectedIndex);
    });

    function doPlayListItemsVideosChanged(index){
        if (index > -1) {
            $('#VideoUp').prop('disabled', false);
            $('#VideoDown').prop('disabled', false);
            $('#VideoRemove').prop('disabled', false);
        }
        else {
            $('#VideoUp').prop('disabled', true);
            $('#VideoDown').prop('disabled', true);
            $('#VideoRemove').prop('disabled', true);
        }

        if (g_playlistitemsVideo.length == 1) {
            $('#VideoUp').prop('disabled', true);
            $('#VideoDown').prop('disabled', true);
        }

        if (index == 0) {
            $('#VideoUp').prop('disabled', true);
        }

        if (index == g_playlistitemsVideo.length - 1) {
            $('#VideoDown').prop('disabled', true);
        }
    }

    $('#selectedMusic').on('change', function () {
        g_playlistitemMusic = g_playlistitemsMusic[this.selectedIndex];
        doPlayListItemsMusicChanged(this.selectedIndex);
    });

    function doPlayListItemsMusicChanged(index){
        if (index > -1) {
            $('#MusicUp').prop('disabled', false);
            $('#MusicDown').prop('disabled', false);
            $('#MusicRemove').prop('disabled', false);
        }
        else {
            $('#MusicUp').prop('disabled', true);
            $('#MusicDown').prop('disabled', true);
            $('#MusicRemove').prop('disabled', true);
        }

        if (g_playlistitemsMusic.length == 1) {
            $('#MusicUp').prop('disabled', true);
            $('#MusicDown').prop('disabled', true);
        }

        if (index == 0) {
            $('#MusicUp').prop('disabled', true);
        }

        if (index == g_playlistitemsMusic.length - 1) {
            $('#MusicDown').prop('disabled', true);
        }
    }

    $('#addVideo2playlist').on('click', function () {
        doAdd2VideoPlaylist();
    })

    $('#addMusic2playlist').on('click', function () {
        doAdd2MusicPlaylist();
    })


    function doFilter() {

        category_SO = -1;
        level_SO = -1;
        background_SO = -1;

        if (g_categorie) {
            category_SO = g_categorie.categories_sort_order;
        }

        if (g_level) {
            level_SO = g_level.levels_sort_order;
        }

        if (g_background) {
            background_SO = g_background.backgrounds_sort_order;
        }

        params = '?categories_SO=' + category_SO;
        params = params + '&levels_SO=' + level_SO;
        params = params + '&backgrounds_SO=' + background_SO;


        $.get("/getVideos" + params, function (data, status) {
            g_videos = JSON.parse(data);
            $('#videos').empty();
            $.each(g_videos, function (i, item) {
                $('#videos').append($('<option>', {
                    value: item.ID,
                    text: item.videos_name
                }));
            });
        });

        $.get("/getMusic" + params, function (data, status) {
            g_music = JSON.parse(data);
            $('#music').empty();
            $.each(g_music, function (i, item) {
                $('#music').append($('<option>', {
                    value: item.ID,
                    text: item.music_name
                }));
            });
        });

        CheckEnabledStatusOfAddButtons();
    }

    function CheckEnabledStatusOfAddButtons(){

        if(g_selectedVideo){
            $('#addVideo2playlist').removeAttr('disabled');
        } 

        if(g_selectedMusic){
            $('#addMusic2playlist').removeAttr('disabled');
        } 
    }

    function doFillPlayListItems(index) {

        params = '?playlist_ID=' + g_playlist.ID;
        $.get("/getPlaylistItems" + params, function (data, status) {
            g_playlistitems = JSON.parse(data);
            $('#playlistitems').empty();
            $.each(g_playlistitems, function (i, item) {
                $('#playlistitems').append($('<option>', {
                    value: item.ID,
                    text: item.videos_name + '-' + item.music_name
                }));
            });
            if (index > -1) {
                $("#playlistitems").prop('selectedIndex', index);
            }
        });
        $('#removePlaylist').removeAttr('disabled');
        $('#editPlaylist').removeAttr('disabled');
    }

    function doFillPlayListItemsMusic(index) {

        params = '?playlist_ID=' + g_playlist.ID;
        $.get("/getPlaylistItemsMusic" + params, function (data, status) {
            g_playlistitemsMusic = JSON.parse(data);
            $('#selectedMusic').empty();
            $.each(g_playlistitemsMusic, function (i, item) {
                category = (item.categories_name + '..............').substring(0, 15) + '|';
                duration = (item.music_duration + 'sec......').substring(0, 7)+ '|';
                string2Display = (category  + ' ' + duration + ' '  + ' ' +  item.music_name).substring(0, 63);
                $('#selectedMusic').append($('<option>', {
                    value: item.ID,
                    text: string2Display
                }));
            });
            if (index > -1) {
                $("#selectedMusic").prop('selectedIndex', index);
            }
        });
        $('#removePlaylist').removeAttr('disabled');
        $('#editPlaylist').removeAttr('disabled');
        $('#play').removeAttr('disabled');
    }


    function doFillPlayListItemsVideo(index) {

        params = '?playlist_ID=' + g_playlist.ID;
        $.get("/getPlaylistItemsVideo" + params, function (data, status) {
            g_playlistitemsVideo = JSON.parse(data);
            $('#selectedVideos').empty();
            $.each(g_playlistitemsVideo, function (i, item) {
                category = (item.categories_name + '..............').substring(0, 15) + '|';
                duration = (item.videos_duration + 'sec......').substring(0, 7)+ '|';
                bg = (item.backgrounds_name + '....').substring(0, 8)+ '|';
                string2Display = (category  + ' ' + duration + ' '  + bg + ' ' +  item.videos_name).substring(0, 63);
                $('#selectedVideos').append($('<option>', {
                    value: item.ID,
                    style: 'white-space: pre-line;',
                    text:  string2Display
                }));
            });
            if (index > -1) {
                $("#selectedVideos").prop('selectedIndex', index);
            }
        });
        $('#removePlaylist').removeAttr('disabled');
        $('#editPlaylist').removeAttr('disabled');
    }



    function doCheck() {
        CheckEnabledStatusOfAddButtons()
    }


    function addPlayList() {
        params = '?playlist_name=' +document.getElementById("playlist_name").value;
        $.get("/addPlaylist" + params, function (data, status) {
            modal.style.display = "none";
            GetPlayLists();
        });
    }

    function editPlayListName() {
        params = '?playlist_name=' +document.getElementById("playlist_name_edit").value;
        params = params + "&playlist_ID="  + g_playlist.ID 
        $.get("/editPlayListName" + params, function (data, status) {
            modalEdit.style.display = "none";
            GetPlayLists();
        });
    }

    function doRemoveFromPlayList() {
        params = '?playlistitem_ID=' + g_playlistitem.pi_ID;

        $.get("/removeFromPlayList" + params, function (data, status) {
            doFillPlayListItems(-1);
        });
    }



    function doMovePlayListItem(tableName, direction) {


        if (tableName == 'playlist_videos'){
            index = $('#selectedVideos').prop('selectedIndex');
            if (index < g_playlistitemsVideo.length) {
                newIndex = index - 1;
            }
            params = '?playlistitem_ID=' + g_playlistitemVideo.pv_ID;
        }else{
            index = $('#selectedMusic').prop('selectedIndex');
            if (index < g_playlistitemsMusic.length) {
                newIndex = index - 1;
            }   
            params = '?playlistitem_ID=' + g_playlistitemMusic.pm_ID;
        }
        
        params = params + '&direction=' + direction;
        params = params + '&tableName=' + tableName;

        $.get("/movePlayListItem" + params, function (data, status) {

            if (tableName == 'playlist_videos'){
                doFillPlayListItemsVideo();
                $('#selectedVideos').selectedIndex = newIndex;
            }
            else{
                doFillPlayListItemsMusic();
                $('#selectedMusic').selectedIndex = newIndex;
            }
        });
    }

    function doRemovePlayListItem(table_name, plItem){
        params = '?table_name=' + table_name;
        if (table_name == 'playlist_videos'){
            params = params + '&playlist_item_ID=' + plItem.pv_ID;
        }
        else{
            params = params + '&playlist_item_ID=' + plItem.pm_ID;
        }
        $.get("/removeFromPlaylist" + params, function (data, status) {
            if (table_name == 'playlist_videos'){
            doFillPlayListItemsVideo(g_playlist.ID);
        }
        else{
            doFillPlayListItemsMusic(g_playlist.ID);
        }
        });
    }

    function doAdd2MusicPlaylist() {
        params = '?playlist_ID=' + g_playlist.ID;
        params = params + '&music_ID=' + g_selectedMusic.ID;
        $.get("/addMusic2PlaylistItems" + params, function (data, status) {
            doFillPlayListItemsMusic(g_playlist.ID);
        });
    }

    function doAdd2VideoPlaylist() {
        params = '?playlist_ID=' + g_playlist.ID;
        params = params + '&video_ID=' + g_selectedVideo.ID;
        $.get("/addVideo2PlaylistItems" + params, function (data, status) {
            doFillPlayListItemsVideo(g_playlist.ID);
        });
    }


    function doRemovePlaylist() {
        params = '?playlist_ID=' + g_playlist.ID;
        $.get("/removePlaylist" + params, function (data, status) {
            $('#playlists').empty();
            GetPlayLists();
        });
    }


    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close");
    span = span[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
