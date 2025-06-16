/* This file is part of the React Unity WebGL Plugin and defines JavaScript functions that can be dispatched from Unity. */

/*
Send the id of the clicked game object to React.
This function is called from Unity when a game object is clicked.
*/
mergeInto(LibraryManager.library, {
  GetData: function (deviceId) {
    dispatchReactUnityEvent("GetData", Pointer_stringify(deviceId));
  },
});

/*
Send the position of the arm to React.
This function is called from Unity when the arm position is changed.
*/
mergeInto(LibraryManager.library, {
  GetArmPos: function (position) {
    dispatchReactUnityEvent("GetArmPos", Pointer_stringify(position));
  },
});
