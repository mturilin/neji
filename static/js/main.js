/**
 * Created with PyCharm.
 * User: mturilin
 * Date: 9/14/12
 * Time: 12:03 PM
 * To change this template use File | Settings | File Templates.
 */

require.config({
    paths: {
        bootstrap: 'bootstrap.min'
    },
    shim: {
        'bootstrap': ['jquery']
    }
});


require(
    ["jquery", "ace/ace", "ace/theme/tomorrow_night", "ace/mode/python", "ace/range","bootstrap"],
    function ($, ace, theme, mode_python, range, bootstrap) {
        "use strict";


        $(function () {
            var editor = ace.edit("editor");
            editor.setTheme("ace/theme/tomorrow_night");
            var PythonMode = mode_python.Mode;
            editor.getSession().setMode(new PythonMode());


            // jQuery Ajax Setup
            var getCookie = function (name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            };

            var csrftoken = getCookie('csrftoken');

            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            $.ajaxSetup({
                crossDomain:false, // obviates need for sameOrigin test
                beforeSend:function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


            $("body").ajaxError(function (event, jqXHR, ajaxSettings, thrownError) {
                alert("Ajax error:" + event);
            });


            // Python execution stuff

            var run_code = function () {
                "use strict";
                var python_code = editor.getValue();
                $.post(
                    "/runpython",
                    {python_code:python_code},
                    function (data) {
                        "use strict";
                        var data_dict = JSON.parse(data);
                        var result_div = $("#python_result");
                        if (!data_dict.error) {
                            result_div.removeClass("alert alert-error");
                            result_div.html(data_dict.output);
                        } else {
                            result_div.addClass("alert alert-error");
                            result_div.html(data_dict.error_message);
                        }
                    });
            };

            $("#run_button").click(function () {
                run_code();

                if (ws) {
                    ws_send({
                        command:"run"
                    });
                }
            });


            var session_mode = $("#session_id").length;

            var session_id = null;
            if (session_mode) {
                session_id = $("#session_id").val();
            }


            $("#new_button").click(function () {
                "use strict";
                var python_code = editor.getValue();
                $.post(
                    "/new",
                    {python_code:python_code},
                    function (data) {
                        "use strict";
                        window.location = data;
                    });
            });

            // WebSocket init
            var ws_url = function () {
                return $("#ws_url").val();
            };

            var ws = null;

            var ws_send = function (dict) {
                if (ws) {
                    ws.send(JSON.stringify(dict));
                }
            };

            var editor_update = false;

            var document_on_change = function (e) {
                if (!editor_update) {

                    ws_send({
                        "command":"update",
                        "action":"delta",
                        "range":editor.getSelection().getRange(),
                        "delta":e.data,
                        "top_row":editor.getFirstVisibleRow(),
                        "text":editor.getValue()
                    });
                }
            };

            var editor_on_change_selection = function () {
                if (!editor_update) {
                    ws_send({
                        "command":"update",
                        "action":"changeSelection",
                        "range":editor.getSelection().getRange(),
                        "top_row":editor.getFirstVisibleRow()
                    });
                }
            };

            var start_web_socket = function () {
                ws = new WebSocket(ws_url());

                ws.onclose = function (evt) {
                    console.log("Connection closed. Restarting...");
                    setTimeout(start_web_socket, 2000)
                    editor.removeEventListener("changeSelection", editor_on_change_selection);
                    editor.getSession().getDocument().removeEventListener("change", document_on_change);

                    $("#socket_status").html("Disconneced from the server").removeClass("alert-success");

                };


                ws.onopen = function () {
                    console.log("WebSocket connected to " + ws_url());

                    // Login as session
                    ws_send({
                        command:"register",
                        session_id:session_id
                    });


                    editor.on("changeSelection", editor_on_change_selection);
                    editor.getSession().getDocument().on("change", document_on_change);

                    $("#socket_status").html("Connected to the server").addClass("alert-success");

                };

                ws.onmessage = function (evt) {
                    "use strict";
                    console.log("Message received: " + evt.data);

                    var message = JSON.parse(evt.data);

                    if (message.command == "update") {
                        editor_update = true;
                        if (message.action == "delta") {
                            editor.getSession().getDocument().applyDeltas([message.delta]);
                            editor.scrollToRow(message.top_row);
                            editor.getSelection().setSelectionRange(message.range);
                        } else if (message.action == "changeSelection") {
                            editor.scrollToRow(message.top_row);
                            editor.getSelection().setSelectionRange(message.range);
                        }

                        editor_update = false;
                    } else if (message.command == "run") {
                        run_code();
                    } else if (message.command == "initial_text") {
                        editor_update = true;
                        editor.setValue(message.text);
                        editor_update = false;
                    } else if (message.command == "initial_range") {
                        editor_update = true;
                        editor.scrollToRow(message.top_row);
                        editor.getSelection().setSelectionRange(message.range);
                        editor_update = false;
                    }
                };
                return editor_update;
            };

            if (session_mode) {
                start_web_socket();
            }

            $('#share_link').popover({
                title: "Sharing link",
                content: "Use this link to invite your friend to edit exactly the same code that you see in your editor",
                trigger: "hover",
                placement: "bottom"
            }).popover("show");

            setTimeout(function() {
                $('#share_link').popover('hide');
            }, 2000)

        });

    });