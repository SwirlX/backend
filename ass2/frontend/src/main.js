import { BACKEND_PORT } from './config.js';
// A helper you may want to use when uploading new images to the server.
import { fileToDataUrl } from './helpers.js';

console.log('Let\'s go!');

const landing_page = document.getElementById("landing_page");

const register_section = document.getElementById("register");
const register_button = document.getElementById("register-button");
const register_email = document.getElementById("register-email");
const register_password = document.getElementById("register-password");
const register_name = document.getElementById("register-name");

const nav_login = document.getElementById("nav-login");
const nav_register = document.getElementById("nav-register");

const login_section = document.getElementById("login");
const login_button = document.getElementById("login-button");
const login_email = document.getElementById("login-email");
const login_password = document.getElementById("login-password");

const logged_in_screen = document.getElementById("logged_in_screen");
const logout_button = document.getElementById("logout-button");
const channels_block = document.getElementById("channels_block");

const public_channels = document.getElementById("public_channels");
const private_channels = document.getElementById("private_channels");
const slackr_heading = document.getElementById("header");
const create_public_channel_button = document.getElementById("create_public_channel_button");
const create_channel_popup_parent = document.getElementById("create_channel_popup_parent");
const channel_create_close = document.getElementById("channel_create_close");
const channel_create_submit = document.getElementById("channel_create_submit");
const create_channel__server_name_input = document.getElementById("server_name_input");
const create_channel__description_input = document.getElementById("description_input");

const create_private_channel_button = document.getElementById("create_private_channel_button");

const channel_form = document.forms.channel_form;
const public_radio = document.getElementById("public_option")
const private_radio = document.getElementById("private_option")

const channel_display_box = document.getElementById("channel_display_box")
const channel_display_top_bar = document.getElementById("channel_display_top_bar")

const channel_name_heading = document.getElementById("channel_name_heading");
const channel_publicity_heading = document.getElementById("channel_publicity_heading");
const channel_description_heading = document.getElementById("channel_description_heading");
const channel_creator_heading = document.getElementById("channel_creator_heading");
const channel_creation_time_heading = document.getElementById("channel_creation_time_heading");



let current_user_token = null;
let current_channel_id = null;
let current_channel_name = null;
let current_channel_desc = null;

const reveal_logged_in_interface = (token, user_id) => {
    current_user_token = token;

    landing_page.style.display = "none";
    console.log("Removing landing page")
    logged_in_screen.style.display = "flex";
    slackr_heading.classList.add("hide");

    display_all_channels(token)
}

const clear_logged_in_screen = () => {
    remove_channels_from_html();
}

const display_all_channels = (token) => {
    const channel_list_promise = retrieve_channel_list(token);

    channel_list_promise.then( (data) => {
        for (const el of data.channels) {
            console.log(el);
        }

        add_channels_to_html(data.channels);
    } )
}

const retrieve_channel_list = (token) => {

    return fetch('http://localhost:5005/channel', {
        method: 'GET',
        headers: {
            'Content-type': 'application/JSON',
            'Authorization': 'Bearer ' + token,
        }

    }).then( (res) => {
        return res.json();
    });

}



const add_channels_to_html = (channels) => {
    remove_channels_from_html()
    for (const channel of channels) {

        const channel_name_div = document.createElement('div');
        channel_name_div.innerText = channel.name
        channel_name_div.classList.add("menu_item");
        channel_name_div.setAttribute('id', channel.name)
        if (channel.private) {
            private_channels.appendChild(channel_name_div);     
        } else {
            public_channels.appendChild(channel_name_div);
        }

        addClickEventToChannelDiv(channel_name_div, channel);

    }

}

const addClickEventToChannelDiv = (channel_name_div, channel) => {
    channel_name_div.addEventListener("click", () => {

            // remove_all_children_tags(channel_display_top_bar)

        const channel_info_promise = fetch_channel_info_promise(channel.id);
        console.log(`fetching info for channel ${channel.id}`);
        current_channel_id = channel.id;
        
        channel_info_promise.then((info_json) => {

            current_channel_name = info_json.name;
            current_channel_desc = info_json.description;

            channel_name_heading.innerText = info_json.name;
            channel_description_heading.innerText = info_json.description;

            const creator_promise = get_user_promise_from_id(info_json.creator);
            creator_promise.then((creator_info)=> {
                channel_creator_heading.innerText = creator_info.name;
            })

            // channel_creator_heading.innerText = info_json.creator;

            channel_publicity_heading.innerText = info_json.private ? "private" : "public";

            const dateObj = new Date(info_json.createdAt)

            console.log(dateObj.toUTCString())
            channel_creation_time_heading.innerText = `Channel created on ${dateObj.toUTCString()}`;
        })

    })
}

const get_user_promise_from_id = (user_id) => {
    
    return fetch(`http://localhost:5005/user/${user_id}`, {
        method: 'GET',
        headers: {
            'Content-type': 'application/JSON',
            'Authorization': 'Bearer ' + current_user_token,
            'userId': user_id,
        }
    }).then( (res) => {
        return res.json();
    });
}

const fetch_channel_info_promise = (channel_id) => {

    return fetch(`http://localhost:5005/channel/${channel_id}`, {
        method: 'GET',
        headers: {
            'Content-type': 'application/JSON',
            'Authorization': 'Bearer ' + current_user_token,
            'channelId': channel_id,
        }

    }).then( (res) => {
        return res.json();
    });
}

const remove_all_children_tags = (parent_tag) => {
    let last_child = parent_tag.lastElementChild;
    while (last_child) {
        parent_tag.removeChild(last_child)
        last_child = parent_tag.lastChild;
    }

}

const remove_channels_from_html = () => {
    // TODO: Fix later

    let public_channel_last= public_channels.lastElementChild;
    while (public_channel_last) {
        public_channels.removeChild(public_channel_last);
        public_channel_last = public_channels.lastChild;
    }

    let private_channel_last= private_channels.lastElementChild;
    while (private_channel_last) {
        private_channels.removeChild(private_channel_last);
        private_channel_last = private_channels.lastChild;
    }
}


const display_login_screen = () => {
    logged_in_screen.style.display = "none";
    landing_page.style.display = "flex";

    register_email.value = "";
    register_password.value = "";
    register_name.value = "";
    login_email.value = "";
    login_password.value = "";
}

const make_request = (route, method, body, fn) => {
    fetch('http://localhost:5005' + route, {
        method: method,
        headers: {
            'Content-type': 'application/JSON'
        },
        body: JSON.stringify(body)
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            // console.log(data);
            fn(data);
            reveal_logged_in_interface(data.token, data.userId);
        }
    });   
}

register_button.addEventListener('click', () => {

    if (!register_email.value || !register_password.value || !register_name.value) {
        alert("Please input your email, password and name");
        return;
    }

    fetch('http://localhost:5005/auth/register', {
        method: 'POST',
        headers: {
            'Content-type': 'application/JSON'
        },
        body: JSON.stringify({
            "email": register_email.value,
            "password": register_password.value,
            "name": register_name.value
        })
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            console.log(data);
            reveal_logged_in_interface(data.token, data.userId);
        }
    });
});


login_button.addEventListener('click', () => {

    if (!login_email.value || !login_password.value) {
        alert("Please input your email and password");
        return;
    }

    fetch('http://localhost:5005/auth/login', {
        method: 'POST',
        headers: {
            'Content-type': 'application/JSON'
        },
        body: JSON.stringify({
            "email": login_email.value,
            "password": login_password.value
        })
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            console.log(data);
            reveal_logged_in_interface(data.token, data.userId);
        }
    });

});

logout_button.addEventListener('click', () => {

    fetch('http://localhost:5005/auth/logout', {
        method: 'POST',
        headers: {
            'Content-type': 'application/JSON',
            'Authorization': 'Bearer ' + current_user_token
        }
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            console.log(data);
            clear_logged_in_screen();
            display_login_screen();
        }
    });

});


nav_login.addEventListener("click", () => {
    console.log("Showing login section")
    register_section.classList.add("hide");
    login_section.classList.remove("hide");
});

nav_register.addEventListener("click", () => {
    console.log("Showing register section")
    login_section.classList.add("hide");
    register_section.classList.remove("hide");
});

create_public_channel_button.addEventListener("click", () => {
    console.log("Create channel menu")
    create_channel_popup_parent.style.display = "flex";
})

create_private_channel_button.addEventListener("click", () => {
    console.log("Create channel menu")
    create_channel_popup_parent.style.display = "flex";
    public_radio.checked = false;
    private_radio.checked = true;

})


channel_create_close.addEventListener("click", () => {
    console.log("Close create channel menu")
    channel_form.reset();
    create_channel_popup_parent.style.display = "none";
})

channel_create_submit.addEventListener("click", () => {

    if (!create_channel__server_name_input.value) {
        alert("Please enter a name for your server");
        console.log("Invalid server name")
        return;
    }

    fetch('http://localhost:5005/channel', {
        method: 'POST',
        headers: {
            'Content-type': 'application/JSON',
            "Authorization": "Bearer " + current_user_token
        },
        body: JSON.stringify({
            "name": create_channel__server_name_input.value,
            "private": private_radio.checked,
            "description": create_channel__description_input.value
        })
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            console.log(data);
            channel_form.reset();
            create_channel_popup_parent.style.display = "none";
            display_all_channels(current_user_token)
        }
    });

})

document.getElementById("rename_channel_save_btn").addEventListener("click", () => {

    const rename_channel_text_input = document.getElementById("rename_channel_text_input");

    if (!rename_channel_text_input.value) {
        console.log("EMPTY RENAME")
        alert("New channel name cannot be empty")

        return;
    }

    fetch(`http://localhost:5005/channel/${current_channel_id}`, {
        method: 'PUT',
        headers: {
            'Content-type': 'application/JSON',
            "Authorization": "Bearer " + current_user_token,
            "channelId": current_channel_id
        },
        body: JSON.stringify({
            "name": rename_channel_text_input.value,
            "description": current_channel_desc
        })
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            console.log(data);

            const rename_modal = document.getElementById('rename_modal');
            const modal = bootstrap.Modal.getInstance(rename_modal);
            modal.hide();

            channel_name_heading.innerText = rename_channel_text_input.value;
            display_all_channels(current_user_token)
        }
        rename_channel_text_input.value = "";
    });

})

document.getElementById("desc_change_save_btn").addEventListener("click", () => {
    const desc_change_text_input = document.getElementById("desc_change_text_input");

    if (!desc_change_text_input.value) {
        console.log("EMPTY DESCRIPTION")
        alert("New description cannot be empty")
        return;
    }

    fetch(`http://localhost:5005/channel/${current_channel_id}`, {
        method: 'PUT',
        headers: {
            'Content-type': 'application/JSON',
            "Authorization": "Bearer " + current_user_token,
            "channelId": current_channel_id
        },
        body: JSON.stringify({
            "name": current_channel_name.value,
            "description": desc_change_text_input.value
        })
    }).then( (res) => {
        return res.json();
    }).then( (data) => {
        if (data.error) {
            alert(data.error);
            console.log(data);
        } else {
            console.log(data);

            const desc_change_modal = document.getElementById('desc_change_modal');
            const modal = bootstrap.Modal.getInstance(desc_change_modal);
            modal.hide();

            channel_description_heading.innerText = desc_change_text_input.value;
        }
        desc_change_text_input.value = "";
    });

})