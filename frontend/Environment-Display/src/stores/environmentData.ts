import {defineStore} from "pinia";
import {computed, reactive, watch} from "vue";
// @ts-ignore
import {io} from "socket.io-client";

export const useEnvironmentDataStore = defineStore('environmentData', () => {
    const environmentData = reactive(<Map<string, Map<string, any>>>{}); // Room name -> Dict
    const rooms = reactive<Array<Map<string, string>>>({});
    const friendlyNamesMap = reactive({});

    const socket = io("http://localhost:8085");
    socket.on("data", (data: Map<string, Map<string, Map<string, any>>>) => {
        // @ts-ignore
        onUpdate(data.data)
    })


    function onUpdate(data: Map<string, Map<string, any>>) {
        // @ts-ignore
        for (const [roomName, roomData] of Object.entries(data)) {
            // @ts-ignore
            environmentData[roomName] = roomData;
        }
    }

    function getDataForRoom(roomName: string): Map<string, any> | null {
        // @ts-ignore
        return environmentData[roomName] || null
    }

    watch(rooms, (newVal, oldVal) => {
        console.log("Rooms changed")
        for (const i in newVal) {
            const name = newVal[i].name
            const friendly_name = newVal[i].friendly_name
            friendlyNamesMap[name] = friendly_name
        }

    })


    return {environmentData, rooms, onUpdate, getDataForRoom, friendlyNamesMap}
})