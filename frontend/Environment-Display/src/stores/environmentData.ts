import {defineStore} from "pinia";
import {computed, reactive} from "vue";
// @ts-ignore
import {io} from "socket.io-client";

export const useEnvironmentDataStore = defineStore('environmentData', () => {
    const environmentData = reactive(<Map<string, Map<string, any>>>{}); // Room name -> Dict
    const rooms = reactive({});

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

    const friendlyNamesMap = computed(() => {
        let ret = {}
        // @ts-ignore
        for (const [name, friendly_name] of Object.entries(rooms)) {
            console.log(name, friendly_name)
            // @ts-ignore
            ret[name] = friendly_name
        }
        console.log(ret)
        return {"data": ret}
    })


    return {environmentData, rooms, onUpdate, getDataForRoom, friendlyNamesMap}
})