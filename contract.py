import smartpy as sp

FA2 = sp.io.import_script_from_url("https://smartpy.io/templates/fa2_lib.py")

t_mint_voice_params = sp.TRecord(
    voice_metadata=sp.TBytes
)

class Univoice(
    FA2.Fa2Nft,
    FA2.OffchainviewTokenMetadata,
    FA2.Admin,
    FA2.OnchainviewBalanceOf
):
    def __init__(self, administrator):
        FA2.Fa2Nft.__init__(self, metadata=sp.big_map(l=None, tkey=sp.TString, tvalue=sp.TBytes), policy=FA2.OwnerOrOperatorTransfer())
        self.update_initial_storage(
            voice_map=sp.big_map(l={}, tkey=sp.TNat, tvalue=sp.TBytes),
            my_voice=sp.big_map(l={}, tkey=sp.TAddress, tvalue=sp.TList(sp.TNat))
        )
        FA2.Admin.__init__(self, administrator)

    @sp.entry_point
    def mint(self, params):
        sp.set_type(params, t_mint_voice_params)
        token_id = sp.compute(self.data.last_token_id)
        self.data.voice_map[token_id] = params.voice_metadata
        with sp.if_(self.data.my_voice.contains(sp.source)):
            self.data.my_voice[sp.source].push(token_id)
        with sp.else_():
            self.data.my_voice[sp.source] = sp.list(l=[token_id], t=sp.TNat)
        self.data.last_token_id += 1
    
    @sp.onchain_view()
    def list_my_voice(self):
        sp.verify(self.data.my_voice.contains(sp.source), "you have no voice on-chain")
        voice_id_list = self.data.my_voice[sp.source]
        result = sp.compute(sp.list(l=[], t=sp.TRecord(
            id=sp.TNat,
            metadata=sp.TBytes
        )))
        with sp.for_("id", voice_id_list) as id:
            result.push(
                sp.record(
                    id=id,
                    metadata=self.data.voice_map[id]
                )
            )
        
        sp.result(result)


@sp.add_test(name="MintVoice")
def mint_voice_test():
    sc = sp.test_scenario()
    alice = sp.test_account("Alice")
    bob = sp.test_account("Bob")
    contract = Univoice(alice.address)
    sc += contract

    contract.mint(sp.record(voice_metadata=sp.bytes("0x01"))).run(source=bob.address)
    sc.verify(sp.len(contract.data.my_voice[bob.address]) == sp.nat(1))
    sc.verify(contract.data.last_token_id == sp.nat(1))

sp.add_compilation_target("UniVoice", Univoice(administrator=sp.address("tz1YGCkky7A61Tc3edJGnTUHEdaiLuZbR6S5")))