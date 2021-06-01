class Style():

    style_bt_standard = (
    """
    QPushButton {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 20px solid rgb(27, 29, 35);
        background-color: rgb(27, 29, 35);
        text-align: left;
        padding-left: 54px;
    }
    QPushButton[Active=true] {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 20px solid rgb(190, 195, 245);
        border-right: 0px solid rgb(190, 195, 245);
        background-color: rgb(190, 195, 245);
        text-align: left;
        padding-left: 50px;
    }
    QPushButton:pressed {
        background-color: rgb(2, 194, 204);
        border-left: 20px solid rgb(2, 194, 204);
        color:rgb(0,0,0);
    }
    """
    )
