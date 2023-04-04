import {defineStore} from "pinia";
import {computed, reactive, ref, watch} from "vue";
// @ts-ignore
import {io} from "socket.io-client";

export const useEnvironmentDataStore = defineStore('environmentData', () => {
    const environmentData = reactive(<Map<string, Map<string, any>>>{}); // Room name -> Dict
    const rooms = reactive<Array<Map<string, string>>>({});
    const friendlyNamesMap = reactive({});
    const websocketConnected = ref(false);

    const socket = io(":8085");
    socket.on("data", (data: Map<string, Map<string, Map<string, any>>>) => {
        // @ts-ignore
        onUpdate(data.data)
    })

    socket.on("connect", () => {
        websocketConnected.value = true;
    })

    socket.on("disconnect", () => {
        websocketConnected.value = false;
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
        for (const i in newVal) {
            const name = newVal[i].name
            const friendly_name = newVal[i].friendly_name
            friendlyNamesMap[name] = friendly_name
        }

    })


    return {environmentData, rooms, onUpdate, getDataForRoom, friendlyNamesMap, websocketConnected}
})