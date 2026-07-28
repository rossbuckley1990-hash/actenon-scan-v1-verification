package tools

import (
    "context"
    "os"
    "os/exec"
    "github.com/modelcontextprotocol/go-sdk/mcp"
)

// UNGUARDED — must be flagged
func runCommand(ctx context.Context, req *mcp.CallToolRequest, args struct {
    Command string
}) (*mcp.CallToolResult, struct{}, error) {
    out, _ := exec.Command("bash", "-c", args.Command).Output()
    return mcp.NewToolResultText(string(out)), struct{}{}, nil
}

// GUARDED — must NOT be flagged
func safeDelete(ctx context.Context, req *mcp.CallToolRequest, args struct {
    Path string
}) (*mcp.CallToolResult, struct{}, error) {
    if authorizeBool(args.Path) {
        os.Remove(args.Path)
    }
    return mcp.NewToolResultText("ok"), struct{}{}, nil
}

// DEFEATED — result discarded
func riskyDelete(ctx context.Context, req *mcp.CallToolRequest, args struct {
    Path string
}) (*mcp.CallToolResult, struct{}, error) {
    authorizeBool(args.Path)
    os.Remove(args.Path)
    return mcp.NewToolResultText("ok"), struct{}{}, nil
}

func authorizeBool(path string) bool { return len(path) > 0 }

func main() {
    server := mcp.NewServer("test", "1.0")
    mcp.AddTool(server, &mcp.Tool{Name: "run_command"}, runCommand)
    mcp.AddTool(server, &mcp.Tool{Name: "safe_delete"}, safeDelete)
    mcp.AddTool(server, &mcp.Tool{Name: "risky_delete"}, riskyDelete)
}
