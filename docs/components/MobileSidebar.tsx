"use client";

import { useState } from "react";
import { Menu } from "lucide-react";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { NavItem } from "@/lib/markdown";
import { Sidebar } from "./Sidebar";

interface MobileSidebarProps {
  navigation: NavItem[];
}

export function MobileSidebar({ navigation }: MobileSidebarProps) {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden fixed left-4 top-4 z-40"
        >
          <Menu className="h-6 w-6" />
          <span className="sr-only">Toggle menu</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="p-0 max-w-[280px] h-[100dvh] left-0 top-0 translate-x-0 translate-y-0 rounded-none data-[state=open]:duration-0 data-[state=closed]:duration-0 pt-10">
        <DialogTitle className="sr-only">Navigation Menu</DialogTitle>
        <div className="h-full" onClick={() => setOpen(false)}>
          <Sidebar navigation={navigation} />
        </div>
      </DialogContent>
    </Dialog>
  );
}