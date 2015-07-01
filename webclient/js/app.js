(function($) {
    App = {};
    
    App.DEBUG = true;
    
    App.Log = function (msg) {
        if((typeof(console) != "undefined") && (App.DEBUG)) {
            console.log(msg);
        }
    }
    
    App.ErrMsg = function (pre, msg) { this.init(pre, msg); }

    jQuery.extend(App.ErrMsg.prototype, {
        init: function (pre, msg) {
            var self = this;
            self.errmsg = $("<div />", { 'class': 'alert alert-error',
                                       'html': '<strong>'+pre+':</strong> ' + msg });
            var closeButton = $("", { 'class': 'close',
                                      'data-dismiss': 'alert',
                                      'text': '&times;' });
        },
        
        getMessage: function () {
            var self = this;
            return self.errmsg;
        }
    });
    
    App.Main = function () { this.init(); }

    jQuery.extend(App.Main.prototype, {
        init: function () {
            var self = this;
            if ($.cookie('username') && $.cookie('password')) {
                self.username = $.cookie('username');
                self.password = $.cookie('password');
                self.initChat();
            } else {
                App.Log($.cookie('username'));
            }
            
            $("#login form").submit(function (e) { self.login(e); });
            $("#register form").submit(function (e) { self.register(e); });
            $("#compose form").submit(function (e) { self.message(e); });
            $("#msg").ajaxError(function () { $(this).append("error") });
        },
        
        login: function (e) {
            var self = this;
            e.preventDefault();
            self.username = $("input[name='username']", e.target).val()
            self.password = $("input[name='password']", e.target).val()
            App.Log(self.username);
            
            $("#loginBtn", e.target).button('loading');
            $.ajax({url: $(e.target).attr('action'),
                    type: "GET",
                    data: $(e.target).serialize(),
                    dataType: 'jsonp',
                    timeout: 1000,
                    success: function(data) { self.onLoginResponse(data) }
            });
        },
        
        register: function (e) {
            var self = this;
            e.preventDefault();
            self.username = $("input[name='username']", e.target).val()
            self.password = $("input[name='password']", e.target).val()
            
            $("#registerBtn", e.target).button('loading');
            $.ajax({url: $(e.target).attr('action'),
                    type: "GET",
                    data: $(e.target).serialize(),
                    dataType: 'jsonp',
                    timeout: 1000,
                    success: function(data) { self.onRegisterResponse(data) }
            });
        },
        
        poll: function () {
            var self = this;
            $.ajax({url: $("meta[name='chatserviceurl']")[0].content + 'poll',
                    type: "GET",
                    data: {'username': self.username,
                           'password': self.password
                           },
                    dataType: 'jsonp',
                    timeout: 1000,
                    success: function(data) { self.onPollResponse(data) }
            });
        },
        
        message: function (e) {
            var self = this;
            e.preventDefault();
            var input = $("input[name='new_message']");
            $.ajax({url: $("meta[name='chatserviceurl']")[0].content + 'message',
                    type: "GET",
                    data: {'username': self.username,
                           'password': self.password,
                           'to': self.currentConversation,
                           'message': $(input).val()
                           },
                    dataType: 'jsonp',
                    timeout: 1000,
                    success: function(data) { self.onMessageResponse(data) }
            });
            $("input", e.target).val("");
        },
        
        join: function (e) {
            var self = this;
            var conversation_id = $("#joinModal input[name='conversation_id']").val();
            $("joinModal").modal('hide');
            self.currentConversation = conversation_id;
            $.ajax({url: $("meta[name='chatserviceurl']")[0].content + 'join',
                    type: "GET",
                    data: {'username': self.username,
                           'password': self.password,
                           'conversation_id': conversation_id
                           },
                    dataType: 'jsonp',
                    timeout: 1000,
                    success: function(data) { self.onJoinResponse(data) }
            });
        },
        
        onLoginResponse: function (data) {
            var self = this;
            $(".alert").remove();
            $("#loginBtn").button('reset');
            switch (data.status) {
                case 200: self.loginSuccess(data);
                          break;
                default:  self.loginFail(data);
                          break;
            }
            
        },
        
        loginSuccess: function (data) {
            var self = this;
            self.initChat();
            $("#join-modal").show();
        },
        
        loginFail: function (data) {
            var error = new App.ErrMsg("Login failed", data.message);
            $(".inner").prepend(error.getMessage());
        },
        
        onRegisterResponse: function (data) {
            var self = this;
            $(".alert").remove();
            $("#registerBtn").button('reset');
            switch (data.status) {
                case 201: self.registerSuccess(data);
                          break;
                default:  self.registerFail(data);
                          break;
            }
        },
        
        registerSuccess: function (data) {
            var self = this;
            self.initChat();
        },
        
        registerFail: function (data) {
            var error = new App.ErrMsg("Regstration failed", data.message);
            $(".alert").remove();
            $(".inner").prepend(error.getMessage());
        },
        
        onPollResponse: function (data) {
            var self = this;
            self.refreshConversations(data.conversations);
        },
        
        onMessageResponse: function (data) {
            // TODO: handle errors
        },
        
        onJoinResponse: function (data) {
            var self = this;
            
            switch (data.status) {
                case 200: self.joinSuccess(data);
                          break;
                default:  self.joinFail(data);
                          break;
            }
        },
        
        joinSuccess: function() {
            var self = this;
            $("#joinModal").modal('hide');
            self.poller = setInterval(function () {self.poll();}, 1000);
        },
        
        joinFail: function () {
            // TODO: handle errors
        },
        
        initChat: function () {
            var self = this;
            $.cookie('username', self.username);
            $.cookie('password', self.password);
            
            $("#container").show();
            $("#loggedout").hide();
            //$("#compose input").attr('disabled', true);
            $("#compose input").select();
            $("#logout").click(function () { self.logout(); });
            $("#join").click(function () { $('#joinModal').modal('show'); });
            
            $('#joinModal').modal('show');
            $('#joinModalBtn').click(function (e) {self.join(e)});
        },
        
        logout: function () {
            var self = this;
            clearInterval(self.poller);
            $.cookie('username', '');
            $.cookie('password', '');
            $("#container").hide();
            $('#contacts li').remove();
            $('#history li').remove();
            $("#compose input[name='new_message']").val('');
            //$("#compose input").attr('disabled', true);
            $("#loggedout").show();
        },
        
        refreshConversations: function (conversations) {
            var self = this;
            if (conversations.length) {
                $('.conversation-id').html(conversations[0].id);
                self.refreshContacts(conversations[0].contacts);
                self.refreshMessages(conversations[0].messages);
            }
        },
        
        refreshContacts: function (contacts) {
            var self = this;
            $("#contacts li").remove();
            $(contacts).each(function () {
                var li = $("<li />", {
                    'class': 'contact'
                    });
                var username = $("<a />", {
                    'class': 'username',
                    'text': this.username
                    });
                var status = $("<span />", {
                    'class': 'status',
                    'text': " (" + this.status + ")"
                    });
                $(li).append(username);
                $(li).append(status);
                $("#contacts ol").append(li);
            });
        },

        padTime: function (n) {
            if (String(n).length == 1) return "0" + n;
            return String(n);
        },

        getTimeStamp: function (timestamp) {
            var self = this;
            var timestamp = new Date(timestamp * 1000);
            return self.padTime(timestamp.getHours()) + ":" +
                   self.padTime(timestamp.getMinutes()) + ":" +
                   self.padTime(timestamp.getSeconds());
        },

        refreshMessages: function (messages) {
            var self = this;
            $(messages).each(function () {
                var message = $("<li />");
                var from = $("<span />", {
                    'class': 'from',
                    'text': this.from
                });
                var msg = $("<span />", {
                    'class': 'to',
                    'text': this.message
                });
                var timestamp = self.getTimeStamp(this.timestamp);
                var timestamp_string = $("<span />", {
                    'class': 'timestamp',
                    'text': timestamp
                });
                $(message).append(from);
                $(message).append(msg);
                $(message).append(timestamp_string);
                $("#history ol").append(message);
            });
            $("#history").scrollTop($("#history").height());
        }
        
    });

})(jQuery);



$(document).ready(function() {
    var app = new App.Main();
});
