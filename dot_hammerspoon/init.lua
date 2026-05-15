local CLIPLINE_DIR = "/tmp"

hs.urlevent.bind("copyclip", function(_, params)
  if params.id then
    local path = CLIPLINE_DIR .. "/clipline-" .. params.id .. ".txt"
    local f = io.open(path, "rb")
    if not f then
      hs.alert.show("📋 missing payload " .. params.id, 1.0)
      return
    end
    local contents = f:read("*a")
    f:close()
    hs.pasteboard.setContents(contents)
    hs.alert.show("📋 copied", 0.4)
    return
  end
  if params.t then
    hs.pasteboard.setContents(params.t)
    hs.alert.show("📋 copied", 0.4)
  end
end)
