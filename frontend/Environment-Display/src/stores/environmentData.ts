import {defineStore} from "pinia";
import {computed, reactive, ref, watch} from "vue";
// @ts-ignore
import {io} from "socket.io-client";

export const useEnvironmentDataStore = defineStore('environmentData', () => {
    // Old variables were environmentData, rooms, friendlyNamesMap, and websocketConnected
    const state = reactive({
        "environmentData": {},
        "rooms": [],
        "friendlyNamesMap": {},
        "websocketConnected": false
    });

    const socket = io(":8085", {transports: ['websocket']});
    socket.on("data", (data: Map<string, Map<string, Map<string, any>>>) => {
        // @ts-ignore
        onUpdate(data.data)
    })

    socket.on("connect", () => {
        state.websocketConnected = true;
        updateRooms()
    })

    socket.on("disconnect", () => {
        state.websocketConnected = false;
    })

    function updateRooms() {
        // Create a GET request to fetch the list of rooms from the backend and populate data.rooms
        fetch(`${window.location.protocol + "//" + window.location.hostname}:8085/rooms`)
            .then(res => res.json())
            .then(json => state.rooms = json.rooms)
    }

    function onUpdate(data: Map<string, Map<string, any>>) {
        // @ts-ignore
        for (const [roomName, roomData] of Object.entries(data)) {
            // @ts-ignore
            state.environmentData[roomName] = roomData;
        }
    }

    function getDataForRoom(roomName: string): Map<string, any> | null {
        // @ts-ignore
        return state.environmentData[roomName] || null
    }

    watch(state, (newVal, oldVal) => {
        for (const i in newVal.rooms) {
            // @ts-ignore
            const name = newVal.rooms[i].name
            // @ts-ignore
            const friendly_name = newVal.rooms[i].friendly_name
            // @ts-ignore
            state.friendlyNamesMap[name] = friendly_name
        }
    })


    return {state, updateRooms, onUpdate, getDataForRoom}
})