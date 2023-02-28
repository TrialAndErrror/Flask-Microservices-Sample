import {defineConfig} from 'vite'
import react from '@vitejs/plugin-react-swc'
import tsconfigPaths from "vite-tsconfig-paths";
import {resolve} from 'path';


const PORT = 3000;
const projectRootDir = resolve(__dirname);


// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        react(),
        tsconfigPaths(),
    ],
    server: {
        port: 3000
    },
})

