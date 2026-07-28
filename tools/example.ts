import { execSync } from 'child_process';
import * as fs from 'fs';
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server({ name: "t", version: "1" }, { capabilities: { tools: {} } });

// UNGUARDED — must be flagged
server.setRequestHandler(CallToolRequestSchema, async (req) => {
    const cmd = req.params.arguments.cmd as string;
    return { content: [{ type: "text", text: execSync(cmd, { encoding: 'utf-8' }) }] };
});

// GUARDED — must NOT be flagged
server.setRequestHandler(CallToolRequestSchema, async (req) => {
    const path = req.params.arguments.path as string;
    if (isAuthorized(path)) { fs.rmSync(path); }
    return { content: [{ type: "text", text: "ok" }] };
});

// DEFEATED — result discarded
server.setRequestHandler(CallToolRequestSchema, async (req) => {
    const path = req.params.arguments.path as string;
    isAuthorized(path);
    fs.rmSync(path);
    return { content: [{ type: "text", text: "ok" }] };
});

function isAuthorized(path: string): boolean { return path.startsWith('/tmp/'); }
