import {defineStore} from "pinia";
import {reactive} from "vue";
import {io} from "socket.io-client";

export const useEnvironmentDataStore = defineStore('environmentData', () => {
    const environmentData = reactive(<Map<string, Map<string, any>>>{}); // Room name -> Dict
    const rooms = reactive({});

    const socket = io("http://localhost:8085");
    socket.on("data", (data: Map<string, Map<string, Map<string, any>>>) => {
        onUpdate(data.data)
    })


    function onUpdate(data: Map<string, Map<string, any>>) {
        for (const [roomName, roomData] of Object.entries(data)) {
            // @ts-ignore
            environmentData[roomName] = roomData;
        }
    }

    return {environmentData, rooms, onUpdate}
})