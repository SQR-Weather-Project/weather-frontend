import json

from streamlit.components.v1 import html


def send_push(
        icon_path: str,
        sound_path: str,
        title: str,
        body: str,
        tag: str = "",
) -> None:
    js_vars = {
        "title": title,
        "body": body,
        "icon": icon_path,
        "audio": sound_path,
        "tag": tag,
    }
    variables = "\n".join(
        f"var {k} = {json.dumps(v)};" for k, v in js_vars.items()
    )

    ws = """
    const ws = new WebSocket("ws://localhost:8000/ws/notify");
    ws.onmessage = function(event) {
        console.log("🔔 " + event.data);
    };
    """

    script = f"""
    {variables}

    var notificationSent = false;

    Notification.requestPermission().then(perm => {{
        if (perm === 'granted') {{
            notification = new Notification(title, {{
                body: body,
                icon: icon,
                tag: tag
            }});
            new Audio(audio).play();
            notificationSent = true;
        }} else if (perm === 'denied') {{
            console.log('User denied notification permission.');
        }} else if (perm === 'default') {{
            console.log('Permission request dismissed.');
        }} else {{
            console.log('Unknown permission state.');
        }}
    }}).catch(error => {{
        console.error('Notification permission error:', error);
    }});
    
    {ws}
    """

    html(f"<script>{script}</script>", width=0, height=0)


def send_alert(message: str) -> None:
    safe_message = json.dumps(message)
    html(
        f"<script>window.alert({safe_message});</script>",
        width=0,
        height=0
    )
